# -*- coding:utf-8 -*-
from appannieenum import AppannieCountry, OSType, AndroidGameCategory, AndroidFeedType
import settings as _s
import traceback
from loggers import get_logger, get_misfire_logger
from commonutils import get_category_display_name
import time
from retry import retry
from bs4 import BeautifulSoup as Bs
import os
from datetime import datetime, timedelta
import pytz
from crawlexception import NoAccountException
from commonutils import wait_account_to_continue, android_feed_to_order_by, MisfireJob
from thecrawler import AndroidTopListCrawler, AndroidTopListParser, IterateTopAppInsert, CrawledDataPolisher
from db import insert_table_app_ranking
from crawltask.refire_queue import add_re_fire_job


def run_android_top_task(country=AppannieCountry.UNITED_STATE, query_date=None, sub_category_code=None, feed=None):
    if sub_category_code and feed:
        _display_category_name = get_category_display_name(sub_category_code)
        get_logger().info('start specific with %s %s android %s: %s...' % (query_date, country, _display_category_name, feed))
        _do_android_top_list_task(country, sub_category_code, feed, query_date)
        get_logger().info('done specific with %s %s android %s: %s!!' % (query_date, country, _display_category_name, feed))
    else:
        for _category in _s.android_category_to_crawl:
            for _feed in _s.android_feed_to_crawl:
                try:
                    _display_category_name = get_category_display_name(_category)
                    get_logger().info('start with %s %s android %s: %s...' % (query_date, country, _display_category_name, _feed))
                    _do_android_top_list_task(country, _category, _feed, query_date)
                    get_logger().info('done with %s %s android %s: %s!!' % (query_date, country, _display_category_name, _feed))
                except Exception as e:
                    get_logger().info('(android) traceback:\n%s' % traceback.format_exc())
                    get_misfire_logger().info(e.__str__())
                    add_re_fire_job(MisfireJob(query_date, country, OSType.Android, _display_category_name, _feed))
                time.sleep(10)
            time.sleep(20)


@retry(exceptions=Exception, tries=2, delay=2)
def _do_android_top_list_task(country, sub_category_code, feed, query_date=None):
    try:
        _order_by = android_feed_to_order_by(feed)
        _f_name = AndroidTopListCrawler(country, sub_category_code, feed, _order_by,
                                        query_date=query_date, mode=_s.default_crawl_mode).crawl()
        if not _f_name.endswith('html'):
            return
        _f_path = _s.default_data_store_dir + _f_name
        if os.path.isfile(_f_path):
            _result_set = None
            with open(_f_path, encoding='utf-8') as f:
                _html_source = f.read()
                _bs = Bs(_html_source, 'lxml')
                _cntz = pytz.timezone('Asia/Shanghai')
                _date_str = None
                if query_date:
                    _date_str = query_date
                else:
                    _yesterday = datetime.now(_cntz) + timedelta(days=-1)
                    _date_str = _yesterday.strftime('%Y-%m-%d')
                _result_set = retryable_task(_bs, country, _date_str, feed, sub_category_code)
            if _result_set and len(_result_set) > 0:
                CrawledDataPolisher.polish(data=_result_set, os=OSType.Android)
                do_insert_record_to_db(_result_set)
                IterateTopAppInsert(result_set=_result_set, country=country, os_type=OSType.Android).do_insert()
    except Exception as e:
        if e.__class__ == NoAccountException:
            get_logger().error('Error: NoAccountException:\n%s' % e.reason)
            wait_account_to_continue(country, '_do_ios_top_task')
        get_logger().error('traceback:\n%s' % traceback.format_exc())
        raise e


@retry(exceptions=Exception, tries=2, delay=2)
def retryable_task(_bs, country, _date_str, feed, sub_category_code):
    return AndroidTopListParser(_bs, country, _date_str, feed, sub_category_code).parse()


def do_insert_record_to_db(_result_set):
    try:
        insert_table_app_ranking(_result_set)
    except Exception as e:
        get_logger().error('traceback:\n%s' % traceback.format_exc())


if __name__ == '__main__':
    _do_android_top_list_task(AppannieCountry.UNITED_STATE, AndroidGameCategory.CATEGORY_ALL,
                              AndroidFeedType.FEED_FREE, query_date='2018-10-14')
    # run_android_top_task(query_date='2018-09-14')
