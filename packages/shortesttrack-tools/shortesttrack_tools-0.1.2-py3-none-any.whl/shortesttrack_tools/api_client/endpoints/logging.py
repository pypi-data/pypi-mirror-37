from shortesttrack_tools.api_client.endpoints.base_endpoint import BaseEndpoint


class LoggingEndpoint(BaseEndpoint):
    def __init__(self, api_client, script_execution_configuration_id, *args, **kwargs):
        super().__init__(api_client, base=api_client.endpoint_urls.LOGGING_ENDPOINT,
                         script_execution_configuration_id=script_execution_configuration_id, *args, **kwargs)
