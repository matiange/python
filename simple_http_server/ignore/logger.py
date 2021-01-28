# -*- coding: utf-8 -*-
"""


Parameters
----------

Returns
-------

:Author:  MaTianGe
:Create:  2021/1/28 13:20
:Blog:    https://safe.shougang.com.cn
Copyright (c) 2021/1/28, ShouAnYun Group All Rights Reserved.
"""

import sys
import queue
import logging
from threading import Thread

_LOG_LEVEL_ = "INFO"
__cache_loggers = {}

__formatter_ = logging.Formatter(
    fmt='[%(asctime)s]-[%(name)s:%(lineno)d] -%(levelname)-4s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(__formatter_)
_handler.setLevel(_LOG_LEVEL_)

_handlers = []
_handlers.append(_handler)

_msg_cache = queue.Queue(10000)


class CachingLogger(logging.Logger):

    def _call_handlers(self, record):
        super().callHandlers(record)

    def callHandlers(self, record):
        _msg_cache.put((self, record))


def set_level(level: str) -> None:
    global _LOG_LEVEL_
    lv = level.upper()
    if lv in ("DEBUG", "INFO", "WARN", "ERROR"):
        _handler.setLevel(lv)
        _logger_ = get_logger("Logger")
        _logger_.info(f"global logger set to {lv}")
        _LOG_LEVEL_ = lv
        for l in __cache_loggers.values():
            l.setLevel(lv)


def add_handler(handler: logging.Handler) -> None:
    _handlers.append(handler)
    for l in __cache_loggers.values():
        l.addHandler(handler)


def remove_handler(handler: logging.Handler) -> None:
    if handler in _handlers:
        _handlers.remove(handler)
    for l in __cache_loggers.values():
        l.removeHandler(handler)


def set_handler(handler: logging.Handler) -> None:
    _handlers.clear()
    _handlers.append(handler)
    for l in __cache_loggers.values():
        for hdlr in l.handlers:
            l.removeHandler(hdlr)
        l.addHandler(handler)


def get_logger(tag: str = "pythone-simple-http-server") -> logging.Logger:
    if tag not in __cache_loggers:
        __cache_loggers[tag] = CachingLogger(tag, _LOG_LEVEL_)
        for hdlr in _handlers:
            __cache_loggers[tag].addHandler(hdlr)
    return __cache_loggers[tag]


def _log_msg_from_queue():
    while True:
        msg = _msg_cache.get()
        msg[0]._call_handlers(msg[1])


def _log_msg_in_backgrond():
    log_thread = Thread(target=_log_msg_from_queue, name="logging-thread")
    log_thread.daemon = True
    log_thread.start()


_log_msg_in_backgrond()
