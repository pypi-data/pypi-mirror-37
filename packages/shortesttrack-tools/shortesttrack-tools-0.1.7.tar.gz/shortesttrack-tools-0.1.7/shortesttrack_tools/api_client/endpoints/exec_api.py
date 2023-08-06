from shortesttrack_tools.api_client.endpoints.base_endpoint import BaseEndpoint


class ExecAPIEndpoint(BaseEndpoint):
    def __init__(self, api_client, script_execution_configuration_id, *args, **kwargs):
        super().__init__(api_client, base=api_client.endpoint_urls.EXEC_API_SERVICE_ENDPOINT,
                         script_execution_configuration_id=script_execution_configuration_id, *args, **kwargs)
