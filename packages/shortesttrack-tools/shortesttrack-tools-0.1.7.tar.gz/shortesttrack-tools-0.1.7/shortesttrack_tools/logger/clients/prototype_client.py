import json
import os
import socket
from datetime import datetime
from typing import Tuple

from pytz import UTC

from shortesttrack_tools.logger.channels import LogChannel
from shortesttrack_tools.logger.clients.base_logger_client import BaseLoggerClient


class PrototypeLoggerClient(BaseLoggerClient):
    def __init__(self, channel: LogChannel, logger_key: str = os.getenv('PROTOTYPE_LOGGER_KEY')):
        self._pre_installed_logger_key = logger_key
        super().__init__()

        self._channel = channel

        try:
            self._socket = socket.socket()
            self._socket.connect(self._connection_address)
        except Exception:
            self._meta_logger.exception('Error on socket connection to logger service')
        else:
            self._is_connected = True

    def send(self, message: str):
        if self._is_connected:
            serialized_message = self._serialize_message(message)
            # Send messages only if logger is connected
            try:
                self._socket.sendall(serialized_message)
            except Exception:
                self._meta_logger.exception('Error on message send to logger service')
                self._is_connected = False

    def _get_connection_address(self) -> Tuple[str, int]:
        ip = os.getenv('PROTOTYPE_LOGGER_IP')
        port = int(os.getenv('PROTOTYPE_LOGGER_PORT'))
        assert all([ip, port])
        return ip, port

    def _get_key(self):
        return self._pre_installed_logger_key

    def __del__(self):
        self._socket.close()

    def _serialize_message(self, message: str) -> bytes:
        json_message = json.dumps({
            'log_id': self._key,
            'ts': str(datetime.now().astimezone(UTC).isoformat()),
            'ch': self._channel,
            'msg': message,
        })

        json_message += '\n'

        return json_message.encode()
