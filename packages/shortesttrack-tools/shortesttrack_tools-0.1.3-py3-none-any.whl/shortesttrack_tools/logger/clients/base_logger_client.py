import abc

import six


@six.add_metaclass(abc.ABCMeta)
class BaseLoggerClient:
    def __init__(self, *args, **kwargs):
        self._connection_address = self._get_connection_address()
        self._key = self._get_key()

    @abc.abstractmethod
    def send(self, message):
        pass

    @abc.abstractmethod
    def _get_connection_address(self):
        pass

    @abc.abstractmethod
    def _get_key(self):
        pass
