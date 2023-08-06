import json
import os
import socket
from typing import Tuple
from time import time

from shortesttrack_tools.logger.clients.base_logger_client import BaseLoggerClient


class PrototypeLoggerClient(BaseLoggerClient):
    def __init__(self):
        super().__init__()
        self._socket = socket.socket()
        self._socket.connect(self._connection_address)

    def send(self, message: str):
        serialized_message = self._serialize_message(message)
        self._socket.sendall(serialized_message)

    def _get_connection_address(self) -> Tuple[str, int]:
        ip = os.getenv('PROTOTYPE_LOGGER_IP')
        port = int(os.getenv('PROTOTYPE_LOGGER_PORT'))
        assert all([ip, port])
        return ip, port

    def _get_key(self):
        return os.getenv('PROTOTYPE_LOGGER_KEY')

    def __del__(self):
        self._socket.close()

    def _serialize_message(self, message: str) -> bytes:
        json_message = json.dumps({
            'log_id': self._key,
            'ts': str(time()),
            'ch': 'script',
            'msg': message,
        })

        json_message += '\n'

        return json_message.encode()
