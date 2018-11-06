# -*- coding:utf-8 -*-
import pymysql
import settings as _s


def get_db_conn():
    db = None
    try:
        db = pymysql.connect(host=_s.mysql_host, user=_s.mysql_user, passwd=_s.mysql_pwd, db=_s.mysql_db, charset='utf8')
    except Exception as e:
        pass
    return db


class DBConnectionHandler:
    def __init__(self):
        self._db_conn = None
        self._cur = None

    def open_conn(self):
        conn = get_db_conn()
        cur = conn.cursor()
        self._db_conn = conn
        self._cur = cur

    def close_conn(self):
        self._cur.close()
        self._db_conn.close()

    def get_cursor(self):
        return self._cur

    def get_conn(self):
        return self._db_conn
