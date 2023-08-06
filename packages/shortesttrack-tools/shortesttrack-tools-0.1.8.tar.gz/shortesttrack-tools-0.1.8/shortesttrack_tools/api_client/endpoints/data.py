from shortesttrack_tools.api_client.endpoints.base_endpoint import BaseEndpoint
from shortesttrack_tools.functional import cached_property


class DataEndpoint(BaseEndpoint):
    def __init__(self, api_client, script_execution_configuration_id, *args, **kwargs):
        super().__init__(api_client, base=api_client.endpoint_urls.DATA_SERVICE_ENDPOINT,
                         script_execution_configuration_id=script_execution_configuration_id,  *args, **kwargs)

    @cached_property
    def script_content(self) -> bytes:
        return self.request(self.GET, f'script-execution-configurations/'
                                      f'{self._script_execution_configuration_id}/script/content', raw_content=True)

    def get_matrix(self, matrix_id):
        return self.request(self.GET, f'script-execution-configurations/'
                                      f'{self._script_execution_configuration_id}/'
                                      f'matrices/{matrix_id}/data')

    def insert_matrix(self, matrix_id: str, matrix_raw):
        url = f'script-execution-configurations/{self._script_execution_configuration_id}/matrices/{matrix_id}/insert'
        return self.request(self.POST, url, json=matrix_raw, raw_content=True)

    def get_trained_model_download_link(self, trained_model_id) -> bytes:
        return self.request(self.GET, f'trained-models/{trained_model_id}/download', raw_content=True)
