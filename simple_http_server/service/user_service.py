import cx_Oracle
from simple_http_server.log import get_logger
from simple_http_server.util import oracle_conn
from simple_http_server.util.oracle_conn import OracleConn

__logger = get_logger('user_controller')#获取日志

# 1.插入操作
def insert(self,insertParam=[]):
    conn = OracleConn().conn
    cursor = conn.cursor()
    sql = 'insert into SRP_SQ_SO_NO_TMP (SID,STAFF_NAME,IDENTITY_ID,TAKENO_DT,SEX,REVIEW_DT,JOB_STATE,ALLOW_ITEM,TERM_VALIDITY) VALUES(SEQ_SQ_SO_NO_TMP.nextval,:staffName,:identityId,:takenoDt,:sex,:reviewDt,:jobState,:allowItem,:termValidity)'  #
    try:
        # 带参数的插入数据：
        if len(insertParam)==0:
            __logger.info("插入数据参数不能为空！")
        else:
            cursor.prepare(sql)
            result = cursor.executemany(self, insertParam)
            conn.commit()
            print("Insert result:", result)
    except Exception as e:
        conn.rollback()#回滚
        # print("Sql执行出错：{%s} \n%s" %(sql,e))
        __logger.error("Sql执行出错：{%s} \n%s" %(sql,e))
    finally:
        cursor.close()
        conn.close()

#查询
def query():
    #conn = cx_Oracle.connect('srp', 'SRPsrp123456', '10.68.26.119:1521/cpsrpt')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可 用户名/密码@主机ip地址/orcl
    conn = cx_Oracle.connect('srp', 'SRPsrp123456', '10.68.26.119:1521/cpsrpt')
    curs = conn.cursor
    try:
        params = {"sid": 190251, "userState": 1}
        sql = 'SELECT a.IDENTITY_ID,a.STAFF_NAME FROM v_sq_so_no a'  # sql语句
        rr = curs.execute(sql) # (sql,params)
        # row = curs.fetchone()#唯一查询
        fetchall = curs.fetchall()  # 多条查询
        for user in fetchall:
            identityId = user[0]
            userName = user[1]
            print(identityId+"  :   "+userName)
        # print(fetchall)
    except Exception as e:
        print(e)
    finally:
        curs.close()
        conn.close()
        # conn.close()