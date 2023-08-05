from enigma import models, util


class ApiEndpointGroup:
    """Abstract base class for a wrapped API endpoint group."""

    def __init__(self, client):
        self._model_wrapper = models.ModelWrapper(self._model_cls, client)
        self._client = client
        self._api = self._model_cls._api_cls(client)
        for (func_name, method) in [
            ('get', 'get'),
            ('list', 'list'),
            ('create', 'post'),
            ('update', 'put'),
            ('delete', 'delete'),
        ]:
            api_func_name = getattr(self._model_cls, '_{}_api_name'.format(method))
            if api_func_name:
                api_func = getattr(self._api, api_func_name)
                func = getattr(self, '_make_{}_func'.format(func_name))(api_func)
                setattr(self, func_name, func)

    def _make_get_func(self, get_api):
        return models.wrapped(get_api, self._model_wrapper)

    def _make_list_func(self, list_api):
        return models.range_wrapped(list_api, self._model_wrapper)

    def _make_create_func(self, post_api):
        return models.wrapped(lambda **kwargs: post_api(body=kwargs), self._model_wrapper)

    def _make_update_func(self, put_api):
        return models.wrapped(lambda id, **kwargs: put_api(id, body=kwargs),
                              self._model_wrapper)

    def _make_delete_func(self, delete_api):
        return models.wrapped(delete_api, None)


class UsersApi(ApiEndpointGroup):
    """Convenience wrapper around the generated User API."""
    _model_cls = models.User


class CollectionsApi(ApiEndpointGroup):
    """Convenience wrapper around the generated Collection API."""
    _model_cls = models.Collection

    def __init__(self, client):
        super().__init__(client)
        self.list = util.adjust_kwargs(self.list, listify={'has_tag'})


class DatasetsApi(ApiEndpointGroup):
    """Convenience wrapper around the generated Dataset API."""
    _model_cls = models.Dataset

    def __init__(self, client):
        super().__init__(client)
        self.get = util.adjust_kwargs(self.get, defaults={'include_serialids': True})
        self.list = util.adjust_kwargs(
            self.list,
            defaults={'include_serialids': True},
            listify={'filter', 'has_tag', 'parent_collection_id', 'sort'})


class SnapshotsApi(ApiEndpointGroup):
    """Convenience wrapper around the generated Snapshot API."""
    _model_cls = models.Snapshot

    def __init__(self, client):
        super().__init__(client)
        self.get = util.adjust_kwargs(self.get, {'include_serialids': True})


class TagsApi(ApiEndpointGroup):
    """Convenience wrapper around the generated Tag API."""
    _model_cls = models.Tag
