# -*- coding:utf-8 -*-
import settings as _s
from db.db_conn import get_db_conn
from appannieenum import AppRankingDBField, TopAppDBField


def insert_table_app_ranking(result_set):
    _offset = 0
    _key_set = _get_columns(result_set)
    _key_set = list(_key_set)
    _formatted_result_set = []
    for _result in result_set:
        if not is_valid_record(_result):
            _offset = _offset + 1
            continue
        tmp_values = []
        if _offset == 0:
            for _key in _key_set:
                tmp_values.append(_result[_key])
        else:
            for _key in _key_set:
                if _key == AppRankingDBField.FIELD_RANKING:
                    _result[_key] = str(int(_result[_key]) - _offset)
                tmp_values.append(_result[_key])
        _formatted_result = list(map(lambda x: str(x) if x is not None else None, tmp_values))
        _formatted_result_set.append(tuple(_formatted_result))
    _cur = None
    _db_conn = None
    try:
        _db_conn = get_db_conn()
        _cur = _db_conn.cursor()
        _sql = _get_insert_app_ranking_sql(_key_set)
        _cur.executemany(_sql, _formatted_result_set)
        _db_conn.commit()
    finally:
        if _cur:
            _cur.close()
        if _db_conn:
            _db_conn.close()


def _insert_table_x_top_game(result_set, ranking_field, get_sql_fun):
    """  deprecated """
    _offset = 0
    _key_set = _get_columns(result_set)
    _key_set = list(_key_set)
    _formatted_result_set = []
    for _result in result_set:
        if not is_valid_record(_result):
            _offset = _offset + 1
            continue
        tmp_values = []
        if _offset == 0:
            for _key in _key_set:
                tmp_values.append(_result[_key])
        else:
            for _key in _key_set:
                if _key == ranking_field:
                    _result[_key] = str(int(_result[_key]) - _offset)
                tmp_values.append(_result[_key])
        _formatted_result = list(map(lambda x: str(x) if x is not None else None, tmp_values))
        _formatted_result_set.append(tuple(_formatted_result))
    _cur = None
    _db_conn = None
    try:
        _db_conn = get_db_conn()
        _cur = _db_conn.cursor()
        _sql = get_sql_fun(_key_set)
        _cur.executemany(_sql, _formatted_result_set)
        _db_conn.commit()
    finally:
        if _cur:
            _cur.close()
        if _db_conn:
            _db_conn.close()


# deprecated
def insert_ios_top_game(result_set):
    _insert_table_x_top_game(result_set, AppRankingDBField.FIELD_RANKING, _get_insert_ios_top_list_sql)


# deprecated
def insert_android_top_game(result_set):
    _insert_table_x_top_game(result_set, AppRankingDBField.FIELD_RANKING, _get_insert_android_top_list_sql)


def is_valid_record(_record):
    if _record and _record.keys():
        if TopAppDBField.FIELD_COMPANY_ID in _record.keys() and TopAppDBField.FIELD_PUBLISHER_ID in _record.keys():
            if _record[TopAppDBField.FIELD_COMPANY_ID] or _record[TopAppDBField.FIELD_PUBLISHER_ID]:
                return True
    return False


def _get_columns(result_set):
    if not result_set or len(result_set) < 1:
        return None
    _result = result_set[0]
    _key_set = []
    for _key in _result.keys():
        if _key in AppRankingDBField.get_all_fields():
            _key_set.append(_key)
    return _key_set


def _get_insert_top_list_sql(key_set, table_name):
    field_count = len(key_set)
    _value_stubs = ', '.join(['%s'] * field_count)
    sql = 'insert into %s ( %s ) values ( %s )' % (table_name, ', '.join(key_set), _value_stubs)
    skip_fields = []
    duplicate_update_field = [x for x in key_set if x not in skip_fields]
    duplicate_update_sql = list(map(lambda f: '%s=values(%s)' % (f, f), duplicate_update_field))
    duplicate_sql_str = ' on duplicate key update %s ' % (', '.join(duplicate_update_sql))
    sql = sql + duplicate_sql_str
    return sql


# deprecated
def _get_insert_ios_top_list_sql(key_set):
    sql = _get_insert_top_list_sql(key_set, _s.mysql_ios_top_free_table)
    return sql


# deprecated
def _get_insert_android_top_list_sql(key_set):
    sql = _get_insert_top_list_sql(key_set, _s.mysql_android_top_free_table)
    return sql


def _get_insert_app_ranking_sql(key_set):
    sql = _get_insert_top_list_sql(key_set, _s.mysql_app_ranking_table)
    return sql


def tmp_func_query_app_id_list():
    sql = """
    select appannie_app_id, appannie_company_id, appannie_publisher_id, owner_name
    from top_app where app_store_url is null
    order by rand();
    """
    _cur = None
    _db_conn = None
    try:
        _db_conn = get_db_conn()
        _cur = _db_conn.cursor()
        _cur.execute(sql)
        _records = _cur.fetchall()
        if not _records:
            return
        _result = []
        for _record in _records:
            _r = dict()
            _r[AppRankingDBField.FIELD_APP_ID] = _record[0]
            _r[TopAppDBField.FIELD_COMPANY_ID] = _record[1]
            _r[TopAppDBField.FIELD_PUBLISHER_ID] = _record[2]
            _r[TopAppDBField.FIELD_OWNER_NAME] = _record[3]
            _result.append(_r)
        return _result
    finally:
        if _cur:
            _cur.close()
        if _db_conn:
            _db_conn.close()


if __name__ == '__main__':
    _xx = {'ranking': 1, 'appannie_app_id': 'fortnite', 'app_name': 'Fortnite',
           'appannie_company_id': '1000200000000041', 'appannie_publisher_id': None,
           'owner_name': 'Chair Entertainment', 'has_iap': 1, 'ranking_change': 0,
           'sub_category': 'Games', 'release_date_str': '2018-03-15',
           'appannie_crawl_date': '2018-08-28', 'update_time': '2018-08-30', 'feed_type': 'Free',
           'query_date': '2018-08-28', 'last_update_date_str': '2018-08-28'}
    print(_get_insert_top_list_sql(AppRankingDBField.get_all_fields(), _s.mysql_app_ranking_table))
