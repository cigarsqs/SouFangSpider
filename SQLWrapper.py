import pymysql

import settings


class SQLWrapper:

    def __init__(self):
        self.host = settings.SQL_INFO['host']
        self.user = settings.SQL_INFO['user']
        self.passwd = settings.SQL_INFO['passwd']
        self.db = settings.SQL_INFO['db']
        self.port = settings.SQL_INFO['port']
        self.charset = settings.SQL_INFO['charset']

    def get_conn(self):
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port,charset=self.charset)
        return conn

    def conn_close(self, conn = None):
        conn.close()

    def conn_commit(self,conn = None):
        conn.commit()

    def excute_statement(self, sql, data, conn = None):
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            cur.close()
        except pymysql.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print "error in excute sql:" + sql


    def excute_fetch_statument(self, sql, conn):
        cur = conn.cursor()
        try:
            cur.execute(sql)
            cur.close()
            data = cur.fetchone()
            return data
        except pymysql.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print "error in excute sql:" + sql