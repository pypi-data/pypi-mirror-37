from shortesttrack_tools.api_client import BaseApiClient


class BaseEndpoint(object):
    def __init__(self, api_client: BaseApiClient, base, script_execution_configuration_id, *args, **kwargs):
        self._api_client = api_client
        self.endpoint_urls = api_client.endpoint_urls
        self._base = base
        self._script_execution_configuration_id = script_execution_configuration_id
        self.GET = 'GET'
        self.POST = 'POST'
        self.PATCH = 'PATCH'
        self.DELETE = 'DELETE'

    def request(
            self,
            http_method,
            path,
            params=None,
            data=None,
            json=None,
            extra_headers=None,
            raw_content=False,
            files=None
    ):
        kwargs = {
            'http_method': http_method,
            'path': path,
            'params': params,
            'data': data,
            'json': json,
            'base': self._base,
            'basic_auth_tuple': None,
            'sec_id_for_special_token': self._script_execution_configuration_id,
            'extra_headers': extra_headers,
            'raw_content': raw_content,
            'files': files
        }

        return self._api_client.request(**kwargs)
