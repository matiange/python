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
import requests,json
from simple_http_server.log import get_logger
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'http://www.weather.com.cn/textFC/hb.shtml',
    'X-Requested-With':'XMLHttpRequest'
}

#获取sessionId
def parse_page(url):
    logger = get_logger("get_sessionid")
    response = requests.get(url, headers=HEADERS)
    resText = response.text
    # print("回值=======    "+resText)
    resSessionId = json.loads(resText).get('time')
    # print("resSessionId=======    "+resSessionId)
    logger.info("sessionId=======    "+resSessionId)
    return resSessionId

if __name__ == '__main__':
    parse_page("http://cx.mem.gov.cn//cms/html/certQuery/certQuery.do?method=getServerTime")


