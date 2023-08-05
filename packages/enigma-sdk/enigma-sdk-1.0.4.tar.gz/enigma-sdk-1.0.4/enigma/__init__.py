import json
import os

from enigma import swagger_client, models, endpoints
from enigma.models import ApiException


swagger_client.models.SnapshotField.__repr__ = lambda self: '<Field {}>'.format(repr(self.display_name))


class SwaggerClient(swagger_client.ApiClient):
    """An extension to the generated Swagger client that supports Bearer tokens."""

    def __init__(self, enigma_client, path_prefix, *args, **kwargs):
        self.enigma_client = enigma_client
        self.path_prefix = path_prefix.rstrip('/')
        super().__init__(*args, **kwargs)

    def call_api(self, resource_path, method,
                 path_params=None, query_params=None, header_params=None,
                 body=None, post_params=None, files=None, **kwargs):
        if self.path_prefix != '/api':
            if resource_path.startswith('/api'):
                resource_path = resource_path[4:]
            resource_path = self.path_prefix + resource_path
        if header_params is None:
            header_params = {}
        if self.enigma_client.apikey:
            header_params['Authorization'] = 'Bearer ' + self.enigma_client.apikey
        if files and not header_params.get('Content-Type'):
            header_params['Content-Type'] = 'multipart/form-data'
        return super().call_api(resource_path, method, path_params, query_params,
                                header_params, body, post_params, files, **kwargs)


class ApiClient:
    """Entry-point class to all the convenience wrapper APIs."""

    def __init__(self, host, path_prefix='', verify_ssl=True):
        self.apikey = None
        config = swagger_client.Configuration()
        config.host = host.rstrip('/')
        config.verify_ssl = verify_ssl
        self.client = SwaggerClient(self, configuration=config, path_prefix=path_prefix)
        for (name, cls) in [
            ('users', endpoints.UsersApi),
            ('collections', endpoints.CollectionsApi),
            ('datasets', endpoints.DatasetsApi),
            ('snapshots', endpoints.SnapshotsApi),
            ('tags', endpoints.TagsApi),
        ]:
            setattr(self, name, cls(self.client))
        dataset_summary_api = swagger_client.DatasetSummaryApi(self.client)
        self.get_dataset_summary = models.wrapped(dataset_summary_api.api_dataset_summary_get)

    def set_auth(self, apikey=None):
        self.apikey = apikey


class Public(ApiClient):

    def __init__(self):
        super().__init__(host='https://public.enigma.com', path_prefix='/api')
        apikey = os.getenv('ENIGMA_PUBLIC_APIKEY')
        if apikey:
            self.set_auth(apikey)
