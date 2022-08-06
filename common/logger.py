# -*- coding: utf-8 -*-
"""
    Common logger
    author: modorigoon
    since: 0.1.0
"""
import os
import logging.handlers
from common.config import get_opts, get_config

_LOGGER_CONFIG = get_config('log')
log = logging.getLogger(__name__)
_opts = get_opts()

_LEVEL_NAME_VALUE = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10
}

_LOG_LEVEL_NAME = None
if 'l' in _opts and _opts['l']:
    _LOG_LEVEL_NAME = _opts['l']
if _LOG_LEVEL_NAME is None:
    _LOG_LEVEL_NAME = _LOGGER_CONFIG['level']
log.setLevel(_LEVEL_NAME_VALUE[_LOG_LEVEL_NAME])

if _LOGGER_CONFIG['file_name'] is not None:
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    max_bytes = 1024 * 1024 * int(_LOGGER_CONFIG['max_file_size_mb'])
    log_fully_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                  _LOGGER_CONFIG['file_name'])
    handler = logging.handlers.RotatingFileHandler(filename=log_fully_path, maxBytes=max_bytes,
                                                   backupCount=int(_LOGGER_CONFIG['backup_count']))
    handler.setFormatter(formatter)
    log.addHandler(handler)
