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
import cx_Oracle

class OracleConn(object):
    conn = None
    cursor = None
    @classmethod
    def setUpClass(cls):
        cls.conn = cx_Oracle.connect('srp', 'SRPsrp123456', '10.68.26.119:1521/cpsrpt')
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.conn.close()
        cls.cursor.close()

    def __init__(self):
        conn = cx_Oracle.connect('srp', 'SRPsrp123456', '10.68.26.119:1521/cpsrpt')
        self.conn = conn
        self.cursor = conn.cursor()