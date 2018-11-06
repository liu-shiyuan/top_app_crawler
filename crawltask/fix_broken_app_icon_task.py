# -*- coding:utf-8 -*-
from db import BrokenIconReDownloader, get_db_conn
from loggers import get_logger
import traceback
import time
import settings as _s

error_base64_contents = [
    'PGh0bWw+DQo8aGVhZD48dGl0bGU+NTAzIFNlcnZpY2UgVGVtcG9yYXJpbHkgVW5hdmFpbGFibGU8L3RpdGxlPjwvaGVhZD4NCjxib2R5IGJnY29sb3I9IndoaXRlIj4NCjxjZW50ZXI+PGgxPjUwMyBTZXJ2aWNlIFRlbXBvcmFyaWx5IFVuYXZhaWxhYmxlPC9oMT48L2NlbnRlcj4NCjxocj48Y2VudGVyPm5naW54PC9jZW50ZXI+DQo8L2JvZHk+DQo8L2h0bWw+DQo='
]

sql = "select id, icon_url from " + _s.mysql_app_icon_table + " where content = '%s' order by rand()"  # limit 0, 50
sql = sql % error_base64_contents[0]


def fix_app_icon_task():
    db_conn = None
    conn_cur = None
    db_records = None
    downloader = None
    try:
        db_conn = get_db_conn()
        conn_cur = db_conn.cursor()
        downloader = BrokenIconReDownloader()
        downloader.open_conn()
        conn_cur.execute(sql)
        db_records = conn_cur.fetchall()
        if not db_records:
            get_logger().info('no broken icon')
        #while db_records:
        for record in db_records:
            downloader.redownload(record[0], record[1], pre_base64_str=error_base64_contents[0])
            time.sleep(0.1)
            #conn_cur.execute(sql)
            #db_records = conn_cur.fetchall()
        get_logger().info('done this round')
    except Exception as e:
        get_logger().error('traceback:\n%s' % traceback.format_exc())
    finally:
        if db_conn:
            db_conn.close()
        if conn_cur:
            conn_cur.close()
        if downloader:
            downloader.close_conn()


def fix_daily_app_icon_task(query_date):
    db_conn = None
    conn_cur = None
    db_records = None
    downloader = None
    try:
        db_conn = get_db_conn()
        conn_cur = db_conn.cursor()
        downloader = BrokenIconReDownloader()
        downloader.open_conn()
        sql = "select id, icon_url from %s where id in (" \
              "select distinct(icon_id) icon_id from %s where query_date = '%s'" \
              ") and content = '%s'" % \
              (_s.mysql_app_icon_table, _s.mysql_app_ranking_table, query_date, error_base64_contents[0])
        conn_cur.execute(sql)
        db_records = conn_cur.fetchall()
        if not db_records:
            get_logger().info('no broken icon')
        # while db_records:
        for record in db_records:
            downloader.redownload(record[0], record[1], pre_base64_str=error_base64_contents[0])
            time.sleep(0.1)
            # conn_cur.execute(sql)
            # db_records = conn_cur.fetchall()
        get_logger().info('done this round')
    except Exception as e:
        get_logger().error('traceback:\n%s' % traceback.format_exc())
    finally:
        if db_conn:
            db_conn.close()
        if conn_cur:
            conn_cur.close()
        if downloader:
            downloader.close_conn()


if __name__ == '__main__':
    # fix_app_icon_task()
    fix_daily_app_icon_task(query_date='2018-09-27')
