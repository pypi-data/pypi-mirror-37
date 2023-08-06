from shortesttrack_tools.api_client.endpoints.base_endpoint import BaseEndpoint


class DataEndpoint(BaseEndpoint):
    def __init__(self, api_client, script_execution_configuration_id, *args, **kwargs):
        super().__init__(api_client, base=api_client.endpoint_urls.DATA_SERVICE_ENDPOINT,
                         script_execution_configuration_id=script_execution_configuration_id,  *args, **kwargs)
