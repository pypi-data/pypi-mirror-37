from urlobject import URLObject
import os

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

    @classmethod
    def _do_init(cls, host=None):
        if host is None:
            cls.HOST = HOST = URLObject(os.environ.get('HOST', 'https://shortesttrack.com'))
        else:
            cls.HOST = HOST = URLObject(host)

        cls.UAA_SERVICE_ENDPOINT = HOST.add_path('api/uaa')
        cls.OAUTH_SERVICE_ENDPOINT = HOST.add_path('oauth')
        cls.JWTKEY_ENDPOINT = HOST.add_path('oauth_jwtkey')
        cls.METADATA_SERVICE_ENDPOINT = HOST.add_path('api/metadata')
        cls.EXEC_API_SERVICE_ENDPOINT = HOST.add_path('api/execution-metadata/v2')
        cls.EXEC_SCHEDULER_SERVICE_ENDPOINT = HOST.add_path('api/exec-scheduling')
        cls.DATA_SERVICE_ENDPOINT = HOST.add_path('api/data')
