import functools
import itertools
import json
import tempfile

from enigma import swagger_client, tableview, util


BOUNDED_PAGE_SIZE = 20
PAGE_SIZE = 50


def wrapped(func, model_wrapper=None):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return model_wrapper(result) if model_wrapper else result
    return wrapper


def range_wrapped(func, model_wrapper):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return ResourceList(func, model_wrapper, *args, **kwargs)
    return wrapper


class ResourceList:
    def __init__(self, api_func, model_wrapper, *args, **kwargs):
        self.bounded = True
        self.func = api_func
        self.wrapper = model_wrapper
        self.args = args
        self.kwargs = kwargs

        self.cache = []
        self.sparse_cache = {}
        self.total = None
        self._fetch_range(0, BOUNDED_PAGE_SIZE)

    def __bool__(self):
        return bool(self.total)

    def __getitem__(self, key):
        cls_name = type(self).__name__
        if isinstance(key, int):
            if key < 0:
                key += self.total
            if not (0 <= key < self.total):
                raise IndexError('{} index out of range'.format(cls_name))
            obj = self._get_cached(key)
            if obj:
                return obj
            start = len(self.cache) if key < len(self.cache) + PAGE_SIZE else key
            self._fetch_range(start, PAGE_SIZE)
            return self[key]

        elif isinstance(key, slice):
            return self._gen_slice(key)

        msg = '{} indices must be integers or slices, not {}'.format(
            cls_name, type(key).__name__)
        raise TypeError(msg)

    def __iter__(self):
        stop = BOUNDED_PAGE_SIZE if self.bounded else None
        return self[:stop]

    def __len__(self):
        if self.bounded:
            return min(BOUNDED_PAGE_SIZE, self.total)
        return self.total

    def __repr__(self):
        if len(self.cache) > 5:
            return '[{}, ...]'.format(', '.join(repr(r) for r in self.cache[:5]))
        else:
            return '[{}]'.format(', '.join(repr(r) for r in self.cache))

    def _gen_slice(self, key):
        """Generate a sequence of objects in this list as specified by the slice *key*."""
        reverse = bool(key.step and key.step < 0)
        for idx in range(self.total)[key.start:key.stop:key.step]:
            obj = self._get_cached(idx)
            if obj:
                yield obj
                continue
            if reverse:
                start = idx - PAGE_SIZE + 1
            elif idx < len(self.cache) + PAGE_SIZE:
                start = len(self.cache)
            else:
                start = idx
            self._fetch_range(start, PAGE_SIZE)
            yield self._get_cached(idx)

    def _get_cached(self, idx):
        """Return an object in the cache for the given *idx*, or None."""
        if idx < len(self.cache):
            return self.cache[idx]
        return self.sparse_cache.get(idx)

    def _fetch_range(self, start, count):
        """Fetch and cache *count* resources beginning at index *start*."""
        self.kwargs['range'] = 'resources={}-{}'.format(start, start + count - 1)
        try:
            objs = self.func(*self.args, **self.kwargs)
        except ApiException as ex:
            if ex.status == 416:
                return
            raise
        objs = [self.wrapper(o) for o in objs]
        headers = self.wrapper.client.last_response.getheaders()
        total = int(headers['content-range'].split('/')[-1])

        clear_cache = (self.total is not None and total != self.total)
        self.total = total
        if clear_cache:
            if start == 0:
                self.cache = objs
                self.sparse_cache = {}
            else:
                self.cache = []
                self.sparse_cache = {i: obj for i, obj in enumerate(objs, start=start)}
        else:
            self._cache_objects(objs, start)

    def _cache_objects(self, objs, start):
        """Insert *objs* into the cache, starting at the index *start*."""
        if start > len(self.cache):
            self.sparse_cache.update(enumerate(objs, start=start))
            return

        # Remove sparse cache objects that would be overwritten by new batch.
        stop = start + len(objs)
        for idx in range(start, stop):
            self.sparse_cache.pop(idx, None)

        # Bulk-resize cache if needed, then copy new objects into cache.
        self.cache.extend([None] * (stop - len(self.cache)))
        self.cache[start:stop] = objs

        # Move any consecutive objects from sparse cache to cache.
        next_indices = itertools.count(len(self.cache))
        sparse_objs = (self.sparse_cache.pop(i, None) for i in next_indices)
        self.cache.extend(itertools.takewhile(bool, sparse_objs))

    def all(self):
        """Set this list to iterate without bounds, and return itself."""
        self.bounded = False
        return self


class ApiException(swagger_client.rest.ApiException):
    def __init__(self, status=None, reason=None, http_resp=None):
        super().__init__(status, reason, http_resp)
        error = self.body
        if isinstance(error, bytes):
            error = error.decode('utf-8')
        self.error_id = None
        self.message = None
        if error:
            error = json.loads(error)
            self.error_id = error['id']
            self.message = error['message']

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({})".format(self.status)
        if self.body:
            error_message += '\n' + self.body
        return error_message

swagger_client.rest.ApiException = ApiException


class ModelWrapper:
    def __init__(self, model_cls, client):
        self.model_cls = model_cls
        self.client = client

    def __call__(self, swagger_obj):
        return self.model_cls(swagger_obj, self.client)


class SDKModel:
    _model_cls = object
    _wrapped_attrs = {}

    def __init__(self, model, client):
        self._model = model
        self._client = client
        self._api = self._api_cls(client)
        wrapper = ModelWrapper(type(self), client)
        self._get = wrapped(getattr(self._api, self._get_api_name), wrapper)
        self._put = wrapped(getattr(self._api, self._put_api_name), wrapper)
        self._delete = wrapped(getattr(self._api, self._delete_api_name), None)
        for name in self._wrapped_attrs:
            value = getattr(model, name, None)
            if value:
                self._set_wrapped_attr(name, value)

    def _set_wrapped_attr(self, name, value):
        wrapper_cls = self._wrapped_attrs[name]
        if isinstance(wrapper_cls, str):
            wrapper_cls = globals()[wrapper_cls]
        def wrap(value):
            if isinstance(value, dict):
                value = RefModel(**value)
            return wrapper_cls(value, self._client)
        if isinstance(value, list):
            value = [wrap(x) for x in value]
        else:
            value = wrap(value)
        object.__setattr__(self, name, value)

    def _as_body(self):
        """Convert a generated model object to a body object accepted by a PUT call."""
        kwargs = {}
        for attr in self._body_cls.attribute_map:
            value = getattr(self, attr)
            if value is not None:
                kwargs[attr] = value
        return self._body_cls(**kwargs)

    def refresh(self, **kwargs):
        return self._get(self.id, **kwargs)

    def save(self):
        """Save the current state of this model as a PUT call."""
        return self._put(self.id, body=self._as_body())

    def update(self, **kwargs):
        """Update this model with the given values, then save it as a PUT call."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self.save()

    def delete(self):
        """Delete the resource corresponding to this model, as a DELETE call."""
        return self._delete(self.id)

    def __getattr__(self, name):
        if hasattr(self._model, name):
            return getattr(self._model, name)
        if hasattr(self._model_cls, name):
            if not hasattr(self, '_full_model'):
                self._full_model = self.refresh()
            return getattr(self._full_model, name)
        msg = "'{}' object has no attribute '{}'".format(type(self).__name__, name)
        raise AttributeError(msg)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        elif name in self._wrapped_attrs:
            self._set_wrapped_attr(name, value)
        else:
            setattr(self._model, name, value)


class Collection(SDKModel):
    """Convenience wrapper around generated Collection models."""

    _api_cls = swagger_client.CollectionApi
    _body_cls = swagger_client.Body1
    _model_cls = swagger_client.Collection
    _wrapped_attrs = {
        'ancestors': 'Collection',
        'parent_collection': 'Collection',
    }

    _get_api_name = 'api_collections_collection_id_get'
    _list_api_name = 'api_collections_get'
    _post_api_name = 'api_collections_post'
    _put_api_name = 'api_collections_collection_id_put'
    _delete_api_name = 'api_collections_collection_id_delete'

    def _as_body(self):
        """Convert a generated model object to a body object accepted by a PUT call."""
        kwargs = {}
        for attr in self._body_cls.attribute_map:
            value = getattr(self, attr)
            if value is not None or attr == 'parent_collection':
                kwargs[attr] = value
        return kwargs

    def create_collection(self, **kwargs):
        kwargs['parent_collection'] = {'id': self.id}
        return self._client.enigma_client.collections.create(**kwargs)

    def create_dataset(self, **kwargs):
        kwargs['parent_collection'] = {'id': self.id}
        return self._client.enigma_client.datasets.create(**kwargs)

    def child_collections(self, **kwargs):
        kwargs['parent_collection_id'] = self.id
        return self._client.enigma_client.collections.list(**kwargs)

    def child_datasets(self, **kwargs):
        kwargs['parent_collection_id'] = self.id
        return self._client.enigma_client.datasets.list(**kwargs)

    def __repr__(self):
        return '<Collection {}>'.format(repr(self.display_name))


class Dataset(SDKModel):

    _api_cls = swagger_client.DatasetApi
    _body_cls = swagger_client.Body3
    _model_cls = swagger_client.Dataset
    _wrapped_attrs = {
        'ancestors': Collection,
        'current_snapshot': 'Snapshot',
        'parent_collection': Collection,
    }

    _get_api_name = 'api_datasets_dataset_id_get'
    _list_api_name = 'api_datasets_get'
    _post_api_name = 'api_datasets_post'
    _put_api_name = 'api_datasets_dataset_id_put'
    _delete_api_name = 'api_datasets_dataset_id_delete'

    def __init__(self, model, client):
        super().__init__(model, client)
        snap_wrapper = ModelWrapper(Snapshot, client)
        self._post_snap = wrapped(self._api.api_datasets_dataset_id_snapshots_post,
                                  snap_wrapper)
        list_snaps = util.adjust_kwargs(
            self._api.api_datasets_dataset_id_snapshots_get, listify={'sort'})
        self._list_snaps = range_wrapped(list_snaps, snap_wrapper)

    def create_snapshot(self, snap, **kwargs):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json') as fp:
            json.dump(snap, fp)
            fp.flush()
            return self._post_snap(self.id, fp.name)

    def snapshots(self, **kwargs):
        return self._list_snaps(self.id, **kwargs)

    def __repr__(self):
        return '<Dataset {}>'.format(repr(self.display_name))


class Snapshot(SDKModel):

    _api_cls = swagger_client.SnapshotApi
    _body_cls = swagger_client.Body9
    _model_cls = swagger_client.Snapshot
    _wrapped_attrs = {
        'dataset': Dataset,
        'parent_snapshot': 'Snapshot',
    }

    _get_api_name = 'api_snapshots_snapshot_id_get'
    _list_api_name = None
    _post_api_name = None
    _put_api_name = 'api_snapshots_snapshot_id_put'
    _delete_api_name = 'api_snapshots_snapshot_id_delete'

    def __init__(self, model, client):
        super().__init__(model, client)
        if getattr(model, 'table_rows', None):
            self.table_rows = tableview.TableView(self, model.table_rows)
        else:
            self.table_rows = None

    def get_rows(self, **kwargs):
        """Return refreshed table rows for this snapshot."""
        if kwargs.get('row_limit') is None:
            kwargs['row_limit'] = 200
        return self.refresh(**kwargs).table_rows

    def export_stream(self, **kwargs):
        """Return a streaming urllib3.HTTPResponse object for the requested export."""
        return self._client.call_api(
            '/api/export/{}'.format(self.id),
            'GET',
            query_params=kwargs,
            _return_http_data_only=True,
            _preload_content=False,
        )

    def export_to(self, path_or_file, **kwargs):
        if isinstance(path_or_file, (str, bytes)):
            with open(path_or_file, 'wb') as fp:
                return self.export_to(fp, **kwargs)
        else:
            write = path_or_file.write
            for chunk in self.export_stream(**kwargs):
                write(chunk)

    def export_dataframe(self, **kwargs):
        try:
            import pandas as pd
        except ModuleNotFoundError:
            raise ModuleNotFoundError("pandas is not installed")
        return pd.read_csv(self.export_stream(**kwargs))

    def __repr__(self):
        return '<Snapshot {}>'.format(repr(self.id))


class Tag(SDKModel):
    """Convenience wrapper around generated Tag models."""

    _api_cls = swagger_client.TagsApi
    _model_cls = swagger_client.Tag

    _get_api_name = 'api_tags_tag_id_get'
    _list_api_name = 'api_tags_get'
    _post_api_name = 'api_tags_post'
    _put_api_name = 'api_tags_tag_id_put'
    _delete_api_name = 'api_tags_tag_id_delete'

    def collections(self, **kwargs):
        kwargs['has_tag'] = self.name
        return self._client.enigma_client.collections.list(**kwargs)

    def datasets(self, **kwargs):
        kwargs['has_tag'] = self.name
        return self._client.enigma_client.datasets.list(**kwargs)

    def __repr__(self):
        return '<Tag {}>'.format(repr(self.name))


class User(SDKModel):
    """Convenience wrapper around generated User models."""

    _body_cls = swagger_client.Body13
    _api_cls = swagger_client.UserApi
    _get_api_name = 'api_users_user_uuid_get'
    _list_api_name = 'api_users_get'
    _post_api_name = 'api_users_post'
    _put_api_name = 'api_users_user_uuid_put'
    _delete_api_name = 'api_users_user_uuid_delete'

    def __repr__(self):
        return '<User {!r}>'.format(self.user_email)

    def add_role(self, role):
        self.roles.append(swagger_client.models.apiusers_roles.ApiusersRoles(role))

    def remove_role(self, role):
        self.roles = [r for r in self.roles if r.role != role]

    def set_roles(self, roles):
        self.roles = [swagger_client.models.apiusers_roles.ApiusersRoles(role) for role in roles]


class RefModel:
    def __init__(self, id, **kwargs):
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)
