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
import re
import datetime
from urllib import parse

import json
import requests
from lxml import etree

from simple_http_server.entity.user import User
from simple_http_server.util import get_sessionId
from simple_http_server.util import tezhong_getcheckcode
GET_DATA = []#抓取的数据集合
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'http://www.weather.com.cn/textFC/hb.shtml'
}

getDataUrl = "http://cx.mem.gov.cn/cms/html/certQuery/certQuery.do?method=getCertQueryResult&ref=ch&certtype_code=720"
getSessionUrl = "http://cx.mem.gov.cn//cms/html/certQuery/certQuery.do?method=getServerTime"
#获取sessionId
def parse_page(idCard,userName):
    USER_LIST = []
    userName = parse.quote(parse.quote(userName))#转码
    #1：获取验证码
    passcode = tezhong_getcheckcode.testChekCode(idCard)
    #2：获取sessionId
    sessionId = get_sessionId.parse_page(getSessionUrl)
    url = getDataUrl+"&certnum="+idCard+"&stu_name="+userName+"&passcode="+passcode+"&sessionId="+sessionId
    print("请求地址===="+url)
    response = requests.get(url, headers=HEADERS)
    resText = response.text
    #3： 获取html
    html_element = etree.HTML(resText)
    #4：解析html文件
    tableList = html_element.xpath('//table[@class="datalist"]')
    for table in tableList:
        thList = table.findall('.//th[@scope][@width]')#过滤出th中包含scope和width属性的
        tdList = table.findall('.//td')
        # 一条条遍历所有td里的内容
        user = User()
        for index, td in enumerate(tdList):
            indexFlag = index+1
            th = thList[index]
            # if index >= 10:
            #     th = thList[indexFlag]
            if td.text is not None and th.text is not None:

                if th.text == '姓名':
                    user.__setattr__("staffName",re.sub('\s','',td.text))
                    user.__setattr__("identityId",re.sub('\s','',idCard))
                    # messageData["identityId"]=re.sub('\s','',idCard)

                if th.text == '性别':
                    user.__setattr__("sex", re.sub('\s', '', td.text))

                if th.text == '初次发证日期':
                    takenoDt = datetime.datetime.strptime(re.sub('\s', '', td.text), "%Y-%m-%d")
                    user.__setattr__("takenoDt", takenoDt)

                if th.text == '应复审日期':
                    reviewDt = datetime.datetime.strptime(re.sub('\s', '', td.text), "%Y-%m-%d")
                    user.__setattr__("reviewDt",reviewDt)

                if th.text == '有效期结束时间':
                    termValidity = datetime.datetime.strptime(re.sub('\s', '', td.text), "%Y-%m-%d")
                    user.__setattr__("termValidity", termValidity)

                if th.text == '操作项目':
                    user.__setattr__("allowItem", re.sub('\s', '', td.text))

                if th.text == '作业类别':
                    user.__setattr__("jobState", re.sub('\s', '', td.text))


                if indexFlag % 10 == 0:
                    USER_LIST.append(user)
                    user = User()
                # print("第"+str(index)+"===   "+th.text+":"+re.sub('\s','',td.text))

    #排序获取有效期最大的数据
    # 第二种方法,更适合于大量数据的情况.
    try:
        import operator
    except ImportError:
        cmpfun = lambda x: x.count  # use a lambda if no operator module
    else:
        cmpfun = operator.attrgetter("termValidity")  # 根据按有效日期排序降序排列
    USER_LIST.sort(key=cmpfun, reverse=True)
    GET_DATA.append(USER_LIST[0].__dict__)#过去最大有效期的数据
    return GET_DATA

if __name__ == '__main__':
    GET_DATA = parse_page("232700198803190012","尤奕雯")
    print(json.dumps(GET_DATA,ensure_ascii=False))
