# -*- coding:utf-8 -*-
import settings as _s
from db.db_conn import DBConnectionHandler
from appannieenum import TopAppDBField


class TopAppDBHandler(DBConnectionHandler):
    def __init__(self):
        super().__init__()

    def insert_record(self, record):
        _sql = self._get_insert_str_sql(record)
        super().get_cursor().execute(_sql, tuple(record.values()))
        super().get_conn().commit()

    def query_record_by_app_id(self, app_id):
        _sql = self._get_query_str_sql(app_id)
        super().get_cursor().execute(_sql)
        data = super().get_cursor().fetchone()
        ret = None
        if data:
            col_names = [t[0] for t in super().get_cursor().description]
            col_count = len(data)
            ret = dict()
            for idx in range(0, col_count):
                ret[col_names[idx]] = data[idx]
        return ret

    def query_record_by_unified_app_id(self, unified_app_id):
        _sql = 'select * from %s where unified_app_id = "%s";' % (_s.mysql_top_app_table, unified_app_id)
        super().get_cursor().execute(_sql)
        data = super().get_cursor().fetchone()
        ret = None
        if data:
            col_names = [t[0] for t in super().get_cursor().description]
            col_count = len(data)
            ret = dict()
            for idx in range(0, col_count):
                ret[col_names[idx]] = data[idx]
        return ret

    def update_record(self, record, update_columns):
        _sql = self._get_update_str_sql(record, update_columns)
        super().get_cursor().execute(_sql)
        super().get_conn().commit()

    @staticmethod
    def _get_query_str_sql(app_id):
        return 'select * from %s where appannie_app_id = "%s";' % (_s.mysql_top_app_table, app_id)

    @staticmethod
    def _get_update_str_sql(record, update_columns):
        _keys = record.keys()
        set_sql_elements = []
        for _key in _keys:
            if _key in update_columns:
                set_sql_elements.append('%s = "%s"' % (_key, record[_key]))
        update_column_count = len(set_sql_elements)
        set_sql_stubs = ', '.join(['%s'] * update_column_count)
        set_sql_block = set_sql_stubs % tuple(set_sql_elements)
        _sql = 'update %s set %s where %s = "%s";' % (_s.mysql_top_app_table,
                                                   set_sql_block,
                                                   TopAppDBField.FIELD_APP_ID,
                                                   record[TopAppDBField.FIELD_APP_ID])
        return _sql

    @staticmethod
    def _get_insert_str_sql(record):
        _keys = record.keys()
        _joined_keys = ', '.join(_keys)
        _count = len(_keys)
        _value_stubs = ', '.join(['%s'] * _count)
        return 'insert into %s (%s) values (%s);' % (_s.mysql_top_app_table, _joined_keys, _value_stubs)


if __name__ == '__main__':
    x = TopAppDBHandler()
    # x.open_conn()
    # ret = x.query_record_by_app_id('-wifi')
    # print(str(ret))

    # record = dict()
    # record[TopAppDBField.FIELD_STORE_URL] = "good"
    # record[TopAppDBField.FIELD_LAST_UPDATE_DATE] = '2018-08-11'
    # record[TopAppDBField.FIELD_APP_ID] = '-wifi'
    # sql = x._get_update_str_sql(record, [TopAppDBField.FIELD_STORE_URL, TopAppDBField.FIELD_LAST_UPDATE_DATE])
    # print(sql)

    # x.close_conn()

