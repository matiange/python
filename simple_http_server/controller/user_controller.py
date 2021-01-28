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
import json
import time
from simple_http_server import request_map, Request
from simple_http_server import Response
from simple_http_server import JSONBody
from simple_http_server.util import getdata_response
from simple_http_server.log import get_logger
from simple_http_server.entity import user
from simple_http_server.service import user_service


@request_map("/index")
def your_ctroller_function():
    # __logger = get_logger('user_controller')
    # __logger.info("访问成功")
    # __logger.warn("测试警告")
    return "<html><body>Python Welcome,Hello World!</body></html>"


@request_map("/say_hello")
def say_hello(res=Response()):
    ##
    # Response 对象就是上述我们写在返回的那个对象，所以，上面的对 headers、cookies 等的接口这个对象均有。
    res.body = "<html><body>Hello, world! </body></html>"
    res.send_response()
    # 如果使用 res 来发送请求，就不再在控制器函数中返回任何内容了。


# 特征作业人员证书抓取接口
@request_map("/get_tzdata", method=["GET", "POST"])
def your_ctroller_function(data=JSONBody(),res=Response()):
    getdata_response.GET_DATA = []#清空一下全局变量
    userList = data.get("userList")
    if len(userList) > 0:
        for user in userList:
            print(user['userName']+"  :  "+user['identityId'])
            #调用抓取数据方法
            getdata_response.parse_page(user['identityId'],user['userName'])
            time.sleep(3)#五秒
    #批量插入数据调用接口：
    user_service.insert(None,getdata_response.GET_DATA)
    # res.body = json.dumps(getdata_response.GET_DATA,ensure_ascii=False)
    res.body = "<html><body>操作成功!</body></html>"
    res.send_response()

@request_map("/")
def redirect(res=Response()):
    res.send_redirect("/index")
