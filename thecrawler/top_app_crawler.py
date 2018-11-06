# -*- coding:utf-8 -*-
import time
from random import randint
import settings as _s
from appannieenum import OSType, TopAppDBField, AppRankingDBField, AndroidGameCategory, IOSGameCategory, \
    AppannieCountry, ios_game_category_names, android_game_category_names
from loggers import get_logger
from thecrawler import AppStoreUrlCrawler
from db import TopAppDBHandler, is_valid_record
from commonutils import get_category_display_name
from datetime import datetime
import pytz

_android_category_all = get_category_display_name(AndroidGameCategory.CATEGORY_ALL)
_ios_category_all = get_category_display_name(IOSGameCategory.CATEGORY_ALL)
_g_category_all = set([_android_category_all, _ios_category_all])
_ios_category_names = [ele['display'] for ele in ios_game_category_names]
_android_category_names = [ele['display'] for ele in android_game_category_names]
_category_names = set(_ios_category_names + _android_category_names)


class IterateTopAppInsert:
    def __init__(self, result_set, country=AppannieCountry.UNITED_STATE, os_type=OSType.IOS):
        self._result_set = result_set
        self._country = country
        self._os_type = os_type
        self._my_date_format = '%Y-%m-%d %H:%M:%S'

    def do_insert(self):
        top_app_handler = None
        url_crawler = None
        top_app_db_fields = TopAppDBField().get_all_fields()
        try:
            top_app_handler = TopAppDBHandler()
            top_app_handler.open_conn()
            url_crawler = AppStoreUrlCrawler(country=self._country, os_type=self._os_type)
            url_crawler.open_conn()
            for _record in self._result_set:
                if not is_valid_record(_record):
                    if _record[AppRankingDBField.FIELD_APP_ID]:
                        get_logger().info('crawling store url: ignore invalid app [%s: %s]' % (
                            _record[AppRankingDBField.FIELD_APP_ID], _record[TopAppDBField.FIELD_APP_NAME]))
                    continue
                db_record = top_app_handler.query_record_by_app_id(_record[TopAppDBField.FIELD_APP_ID])
                if db_record:
                    update_columns = []
                    if not db_record[TopAppDBField.FIELD_STORE_URL]:
                        store_url = url_crawler.crawl_store_url(_record, lambda: time.sleep(
                            _s.store_url_crawl_interval + randint(0, 5)))
                        if store_url:
                            db_record[TopAppDBField.FIELD_STORE_URL] = store_url
                            update_columns.append(TopAppDBField.FIELD_STORE_URL)
                    if db_record[TopAppDBField.FIELD_LAST_UPDATE_DATE] < _record[TopAppDBField.FIELD_LAST_UPDATE_DATE]:
                        db_record[TopAppDBField.FIELD_LAST_UPDATE_DATE] = _record[TopAppDBField.FIELD_LAST_UPDATE_DATE]
                        update_columns.append(TopAppDBField.FIELD_LAST_UPDATE_DATE)
                    if _record[TopAppDBField.FIELD_CATEGORY] and _record[
                            TopAppDBField.FIELD_CATEGORY] not in _g_category_all:
                        db_category = db_record[TopAppDBField.FIELD_CATEGORY]
                        db_categories = db_category.split(',') if db_category else []
                        if _record[TopAppDBField.FIELD_CATEGORY] not in db_categories and _record[
                                TopAppDBField.FIELD_CATEGORY] in _category_names:
                            db_categories.append(_record[TopAppDBField.FIELD_CATEGORY])
                            new_category = ','.join(db_categories)
                            db_record[TopAppDBField.FIELD_CATEGORY] = new_category
                            update_columns.append(TopAppDBField.FIELD_CATEGORY)
                    elif _record[AppRankingDBField.FIELD_QUERY_CATEGORY] and _record[
                            AppRankingDBField.FIELD_QUERY_CATEGORY] not in _g_category_all:
                        db_category = db_record[TopAppDBField.FIELD_CATEGORY]
                        db_categories = db_category.split(',') if db_category else []
                        if _record[AppRankingDBField.FIELD_QUERY_CATEGORY] not in db_categories and _record[
                                AppRankingDBField.FIELD_QUERY_CATEGORY] in _category_names:
                            db_categories.append(_record[AppRankingDBField.FIELD_QUERY_CATEGORY])
                            new_category = ','.join(db_categories)
                            db_record[TopAppDBField.FIELD_CATEGORY] = new_category
                            update_columns.append(TopAppDBField.FIELD_CATEGORY)
                    if _record[TopAppDBField.FIELD_UNIFIED_APP_ID] and _record[TopAppDBField.FIELD_UNIFIED_APP_ID] != \
                            db_record[TopAppDBField.FIELD_UNIFIED_APP_ID]:
                            db_record[TopAppDBField.FIELD_UNIFIED_APP_ID] = _record[TopAppDBField.FIELD_UNIFIED_APP_ID]
                            update_columns.append(TopAppDBField.FIELD_UNIFIED_APP_ID)
                    if update_columns:
                        get_logger().info('updating top app %s for (%s)' %
                                          (db_record[TopAppDBField.FIELD_APP_ID], ', '.join(update_columns)))
                        update_columns.append(TopAppDBField.FIELD_UPDATE_TIME)
                        db_record[TopAppDBField.FIELD_UPDATE_TIME] = datetime.now(pytz.timezone('Asia/Shanghai')) \
                            .strftime(self._my_date_format)
                        top_app_handler.update_record(db_record, update_columns)
                else:
                    tmp_record = dict()
                    for _key in _record.keys():
                        if _key in top_app_db_fields and _key not in \
                                [TopAppDBField.FIELD_STORE_URL, TopAppDBField.FIELD_UPDATE_TIME]:
                            tmp_record[_key] = _record[_key]
                    store_url = url_crawler.crawl_store_url(_record, lambda: time.sleep(
                        _s.store_url_crawl_interval + randint(0, 5)))
                    if store_url:
                        tmp_record[TopAppDBField.FIELD_STORE_URL] = store_url
                    tmp_record[TopAppDBField.FIELD_UPDATE_TIME] = datetime.now(pytz.timezone('Asia/Shanghai')) \
                        .strftime(self._my_date_format)
                    if tmp_record[TopAppDBField.FIELD_CATEGORY] in _g_category_all \
                        and _record[AppRankingDBField.FIELD_QUERY_CATEGORY] not in _g_category_all \
                        and _record[AppRankingDBField.FIELD_QUERY_CATEGORY] in _category_names:
                            tmp_record[TopAppDBField.FIELD_CATEGORY] = _record[AppRankingDBField.FIELD_QUERY_CATEGORY]
                    top_app_handler.insert_record(tmp_record)
        except Exception as e:
            raise e
        finally:
            if top_app_handler:
                top_app_handler.close_conn()
            if url_crawler:
                url_crawler.close_conn()
