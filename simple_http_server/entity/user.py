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
import datetime
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
#创建连接对象
engine = create_engine("oracle://srp:SRPsrp123456@10.68.26.119:1521/cpsrpt")
# 创建一张表
# 不会重新创建已经存在的表
session_factory = sessionmaker(bind=engine)

class UserInfo(Base):
    """
      定义一张表
      """
    __tablename__ = "SRP_SQ_SO_NO_TMP"
    SID = Column(Integer, primary_key=True,doc='主键', comment='主键', nullable=False)
    STAFF_NAME = Column(String(32),doc='姓名', comment='姓名')
    IDENTITY_ID = Column(String(32),doc='身份证号', comment='身份证号')
    TAKENO_DT = Column(DateTime,doc='取证日期', comment='取证日期')
    SEX = Column(String(4),doc='性别', comment='性别')
    REVIEW_DT = Column(DateTime, doc='复审日期', comment='复审日期')
    JOB_STATE = Column(String(254), doc='作业类别', comment='作业类别')
    ALLOW_ITEM = Column(String(254), doc='准操项目', comment='准操项目')
    TERM_VALIDITY = Column(DateTime, doc='有效日期', comment='有效日期')
    __table_args__ = ({'comment': '特种作业操作证临时表'})  # 添加索引和表注释 --->索引Index('index(zone,status)', 'resource_zone', 'resource_status'),


class User(object):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
    # 构造
    def __init__(self, staffName:str="", identityId:str="", takenoDt:datetime=nowTime, sex:str="", reviewDt:datetime=nowTime, jobState:str="", allowItem:str="", termValidity:datetime=nowTime):
        self.staffName = staffName
        self.identityId = identityId
        self.takenoDt = takenoDt
        self.sex = sex
        self.reviewDt = reviewDt
        self.jobState = jobState
        self.allowItem = allowItem
        self.termValidity = termValidity

    # toString方法
    def __str__(self) -> str:
        return "User\n staffName: %s \t identityId: %s \t takenoDt: %s \t sex: %s \t reviewDt:%s \t jobState: %s \t allowItem: %s \t termValidity: %s" % (self.staffName, self.identityId,self.takenoDt, self.sex, self.reviewDt, self.jobState, self.allowItem, self.termValidity)
    # 对象销毁
    # def __del__(self):
    #     className = self.__class__.__name__
    #     print(className+"销毁了")

#无表自动创建
def main():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()