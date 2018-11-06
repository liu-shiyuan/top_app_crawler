# -*- coding:utf-8 -*-
from crawltask.ios_crawl_task import run_ios_top_task
from crawltask.android_crawl_task import run_android_top_task
from appannieenum import AppannieCountry, IOSGameCategory, IOSFeedType, AndroidGameCategory, AndroidFeedType
from commonutils import get_cst_yesterday
from loggers import get_logger
from crawltask.fix_broken_app_icon_task import fix_daily_app_icon_task

#_query_date = '2018-09-27'
_query_date = get_cst_yesterday()

if __name__ == '__main__':
    get_logger().info('do oneway job with %s' % _query_date)
    run_ios_top_task(country=AppannieCountry.UNITED_STATE, query_date=_query_date,
                     sub_category_code=IOSGameCategory.CATEGORY_ACTION, feed=IOSFeedType.FEED_FREE)
    run_android_top_task(country=AppannieCountry.UNITED_STATE, query_date=_query_date,
                         sub_category_code=AndroidGameCategory.CATEGORY_ACTION, feed=AndroidFeedType.FEED_FREE)
    fix_daily_app_icon_task(_query_date)
    get_logger().info('done oneway job with %s' % _query_date)