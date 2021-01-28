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
import simple_http_server.server as server
# 如果你的控制器代码（处理请求的函数）放在别的文件中，那么在你的 main.py 中，你必须将他都 import 进来。
# import my_test_ctrl


def main(*args):
    # 除了 import 外，还可以通过 scan 方法批量加载 controller 文件。
    server.scan("controller", r".*controller.*")
    # server.start(host="", port=8899)
    server.start()

if __name__ == "__main__":
    main()