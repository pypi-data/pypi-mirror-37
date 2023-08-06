import logging
import sys
from typing import Iterable

from shortesttrack_tools.logger.channels import LogChannel
from shortesttrack_tools.logger.clients.prototype_client import PrototypeLoggerClient
from shortesttrack_tools.logger.handlers.st_handler import STLoggerHandler
from shortesttrack_tools.logger.registry.logger_registry import LoggerRegistry

APPLICATION_LOG_NAME = 'shortesttrack-tools'
PROTOTYPE_LOG_NAME = 'prototype-logger'

DEFAULT_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
PROTOTYPE_FORMATTER = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

LOG_LEVEL = 'INFO'
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(DEFAULT_FORMATTER)
root_logger.addHandler(stream_handler)


def getLogger(name: str = APPLICATION_LOG_NAME, log_level: str = LOG_LEVEL,
              extra_handlers: Iterable[logging.Handler] = None):
    logger = logging.getLogger(name)

    registry = LoggerRegistry.init()
    if id(logger) in registry.logger_ids:
        # Prevent to duplicate handlers and re-installing options
        return logger

    logger.setLevel(log_level)

    if extra_handlers:
        for handler in extra_handlers:
            logger.addHandler(handler)

    registry.logger_ids.add(id(logger))
    return logger


def _get_qualified_name(name: str) -> str:
    if name:
        return f'{APPLICATION_LOG_NAME}.{name}'

    return APPLICATION_LOG_NAME


def get_prototype_logger(
        name: str = PROTOTYPE_LOG_NAME,
        channel: LogChannel = LogChannel.PERFORMANCE.value,
        prototype_formatter=PROTOTYPE_FORMATTER,
        log_level=LOG_LEVEL
):
    client = PrototypeLoggerClient(channel)
    handler = STLoggerHandler(client)
    handler.setFormatter(prototype_formatter)
    _logger = getLogger(name, log_level, [handler])
    return _logger
