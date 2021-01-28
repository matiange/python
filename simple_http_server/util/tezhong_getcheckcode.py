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
import copy
import time
import os
import tesserocr

from simple_http_server.log import get_logger
from simple_http_server.util import check_code
from PIL import Image
from urllib import request
from enum import Enum, unique

_logger = get_logger("tezhong_getcheckcode")

@unique
class DirMode(Enum):
    CONFIG = 0  #配置标识
    PACKAGE = 1 #包路径标识

#验证码图片相关配置
CHECK_CODE_IMG_CONFIG = {
    "check_code_img_dir":"D:/checkCode/",
    "original_code":"D:/checkCode/original_code/",
    "interferencePoint_code":"D:/checkCode/interferencePoint_code/"
}

def check_code_img_config(img_config,dir_mode=DirMode.CONFIG):
    if dir_mode == DirMode.CONFIG:
        dirName = CHECK_CODE_IMG_CONFIG["check_code_img_dir"]
        dirOriginalCode = CHECK_CODE_IMG_CONFIG["original_code"]
        dirInterferencePointCode = CHECK_CODE_IMG_CONFIG["interferencePoint_code"]
    else:
        currentdir = os.path.dirname(__file__).replace('\\', '/')
        dirName = currentdir + '/checkCode/'
        dirOriginalCode = dirName + '/original_code/'
        dirInterferencePointCode = dirName + '/interferencePoint_code/'
        img_config["check_code_img_dir"] = dirName
        img_config["original_code"] = dirOriginalCode
        img_config["interferencePoint_code"] = dirInterferencePointCode
    if dirName is not None:
        if not os.path.exists(dirName):
            try:
                os.makedirs(dirName)

            except Exception as e:
                _logger.error(e)
    if dirOriginalCode is not None:
        if not os.path.exists(dirOriginalCode):
            try:
                os.makedirs(dirOriginalCode)  # 验证码原始文件

            except Exception as e:
                _logger.error(e)

    if dirInterferencePointCode is not None:
        if not os.path.exists(dirInterferencePointCode):
            try:
                os.makedirs(dirInterferencePointCode)  # 验证码去除扰码噪声文件

            except Exception as e:
                _logger.error(e)

    return img_config
# 用parse模块，通过bytes(parse.urlencode())可以将post数据进行转换并放到
# urllib.request.urlopen的data参数中。这样就完成了一次post请求。
def getCheckCode(filePath):
    image = Image.open(filePath)
    # 转为灰度图像
    image = image.convert('L')
    # 二值化
    threshold = 110
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    # image.show()
    result = tesserocr.image_to_text(image)
    return result

##身份证对应验证码
def testChekCode(idCard):
    #深拷贝验证码配置字典
    checkCodeImgConfig = copy.deepcopy(CHECK_CODE_IMG_CONFIG)

    #调用配置生成验证码文件
    check_code_img_config(checkCodeImgConfig,DirMode.PACKAGE)

    date = str(int(time.time()))  # 获取当前时间10位
    data = request.urlopen('http://cx.mem.gov.cn//GetImg?date=' + str(date)).read()
    fileName = "code_" + idCard + ".jpg"
    file = checkCodeImgConfig["original_code"] + fileName
    fileInterferencePath = checkCodeImgConfig["interferencePoint_code"]
    playFile = open(file, 'wb')
    playFile.write(data)
    playFile.close()

    # 去除扰码后图片保留
    check_code.main(file,fileName,fileInterferencePath)

    fileName = "code_" + idCard + "_interferencePoint.jpg"
    filePath = fileInterferencePath + fileName
    checkCode = getCheckCode(filePath)#调用获取验证码的方法
    # print(fileName + "=====" + checkCode)
    # 删除文件
    os.remove(file)#删除原验证码
    os.remove(filePath)#删除扰码
    return checkCode


if __name__ == '__main__':
    testChekCode()
