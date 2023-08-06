from shortesttrack_tools.api_client.endpoints.base_endpoint import BaseEndpoint


class MetadataEndpoint(BaseEndpoint):
    def __init__(self, api_client, script_execution_configuration_id, *args, **kwargs):
        super().__init__(api_client, base=api_client.endpoint_urls.METADATA_SERVICE_ENDPOINT,
                         script_execution_configuration_id=script_execution_configuration_id, *args, **kwargs)

    @property
    def script_execution_configuration(self):
        return self.request(self.GET, f'script-execution-configurations/{self._script_execution_configuration_id}')

    def get_trained_model(self, trained_model_id):
        return self.request(self.GET, f'trained-models/{trained_model_id}')
