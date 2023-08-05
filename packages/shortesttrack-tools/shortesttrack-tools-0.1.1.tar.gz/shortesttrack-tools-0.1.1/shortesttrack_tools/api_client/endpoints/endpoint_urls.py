import os
from urlobject import URLObject

from shortesttrack_tools.unique import Unique


class EndpointURLs(Unique):
    HOST = None

    UAA_SERVICE_ENDPOINT = None
    OAUTH_SERVICE_ENDPOINT = None
    JWTKEY_ENDPOINT = None
    METADATA_SERVICE_ENDPOINT = None
    EXEC_API_SERVICE_ENDPOINT = None
    EXEC_SCHEDULER_SERVICE_ENDPOINT = None
    DATA_SERVICE_ENDPOINT = None
    LOGGING_ENDPOINT = None

    @classmethod
    def _do_init(cls, host: str = None):
        cls.HOST = URLObject(host) if host else URLObject(os.environ.get('HOST', 'https://shortesttrack.com'))

        cls.OAUTH_SERVICE_ENDPOINT = URLObject(os.environ.get('OAUTH_SERVICE_ENDPOINT')) \
            if os.environ.get('OAUTH_SERVICE_ENDPOINT') else cls.HOST.add_path('oauth')

        cls.JWTKEY_ENDPOINT = URLObject(os.environ.get('JWTKEY_ENDPOINT')) \
            if os.environ.get('JWTKEY_ENDPOINT') else cls.HOST.add_path('oauth_jwtkey')

        cls.UAA_SERVICE_ENDPOINT = cls.HOST.add_path('api/uaa')
        cls.METADATA_SERVICE_ENDPOINT = cls.HOST.add_path('api/metadata')
        cls.EXEC_API_SERVICE_ENDPOINT = cls.HOST.add_path('api/execution-metadata/v2')
        cls.EXEC_SCHEDULER_SERVICE_ENDPOINT = cls.HOST.add_path('api/exec-scheduling')
        cls.DATA_SERVICE_ENDPOINT = cls.HOST.add_path('api/data')
        cls.LOGGING_ENDPOINT = cls.HOST.add_path('api/logging')
