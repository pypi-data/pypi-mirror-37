import abc

import six


@six.add_metaclass(abc.ABCMeta)
class BaseLoggerClient:
    def __init__(self, *args, **kwargs):
        from shortesttrack_tools.logger import getLogger
        self._meta_logger = getLogger('prototype-logger-client.meta-logger')
        self._is_connected = False
        try:
            self._connection_address = self._get_connection_address()
            self._key = self._get_key()
        except Exception:
            self._meta_logger.exception('Error on getting logger parameters')

    @abc.abstractmethod
    def send(self, message):
        pass

    @abc.abstractmethod
    def _get_connection_address(self):
        pass

    @abc.abstractmethod
    def _get_key(self):
        pass
