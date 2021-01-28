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

import os
import threading
import inspect
import importlib
import re
import ssl as _ssl

from typing import Dict

import simple_http_server.http_server as http_server

from simple_http_server import _get_filters
from simple_http_server import _get_request_mappings
from simple_http_server import request_map
from simple_http_server import StaticFile
from simple_http_server.ignore.logger import get_logger


__logger = get_logger("simple_http_server.server")
__lock = threading.Lock()
__server = None


def _is_match(string="", regx=r""):
    if not regx:
        return True
    pattern = re.compile(regx)
    match = pattern.match(string)
    return True if match else False


def _to_module_name(fpath="", regx=r""):
    fname, fext = os.path.splitext(fpath)

    if fext != ".py":
        return
    mname = fname.replace(os.path.sep, '.')
    if _is_match(fpath, regx) or _is_match(fname, regx) or _is_match(mname, regx):
        return mname


def _load_all_modules(work_dir, pkg, regx):
    abs_folder = work_dir + "/" + pkg
    all_files = os.listdir(abs_folder)
    modules = []
    folders = []
    for f in all_files:
        if os.path.isfile(os.path.join(abs_folder, f)):
            mname = _to_module_name(os.path.join(pkg, f), regx)
            if mname:
                modules.append(mname)
        elif f != "__pycache__":
            folders.append(os.path.join(pkg, f))

    for folder in folders:
        modules += _load_all_modules(work_dir, folder, regx)
    return modules


def _import_module(mname):
    try:
        importlib.import_module(mname)
    except:
        __logger.warn(f"Import moudle [{mname}] error!")


def scan(base_dir: str = "", regx: str = r"") -> None:
    ft = inspect.currentframe()
    fts = inspect.getouterframes(ft)
    entrance = fts[0]
    # entrance = fts[-1]之前取的是python的安装路径
    work_dir = os.path.dirname(inspect.getabsfile(entrance[0]))
    modules = _load_all_modules(work_dir, base_dir, regx)

    for mname in modules:
        __logger.info(f"Import controllers from module: {mname}")
        _import_module(mname)


def start(host: str = "",
          port: int = 9090,
          ssl: bool = False,
          ssl_protocol: int = _ssl.PROTOCOL_TLS_SERVER,
          ssl_check_hostname: bool = False,
          keyfile: str = "",
          certfile: str = "",
          keypass: str = "",
          ssl_context: _ssl.SSLContext = None,
          resources: Dict[str, str] = {}) -> None:
    with __lock:
        global __server
        if __server is not None:
            __server.shutdown()
        __server = http_server.SimpleDispatcherHttpServer(host=(host, port),
                                                          ssl=ssl,
                                                          ssl_protocol=ssl_protocol,
                                                          ssl_check_hostname=ssl_check_hostname,
                                                          keyfile=keyfile,
                                                          certfile=certfile,
                                                          keypass=keypass,
                                                          ssl_context=ssl_context,
                                                          resources=resources)

    __filters = _get_filters()
    # filter configuration
    for ft in __filters:
        __server.map_filter(ft["url_pattern"], ft["func"])

    __request_mappings = _get_request_mappings()
    # request mapping
    for ctr in __request_mappings:
        __server.map_request(ctr)

    # start the server
    __server.start()


def stop() -> None:
    with __lock:
        global __server
        if __server is not None:
            __logger.info("shutting down server...")
            __server.shutdown()
            __server = None


@request_map("/favicon.ico")
def _favicon():
    root = os.path.dirname(os.path.abspath(__file__))
    return StaticFile(f"{root}/favicon.ico", "image/x-icon")
