# -*- coding:utf-8 -*-
from appannieenum import game_category_names, IOSFeedType, AndroidFeedType, AndroidTopChartOrderBy, IOSTopChartOrderBy
from datetime import datetime, timedelta
import pytz
from urllib import parse
import time
import re


def get_category_display_name(str_category_code):
    if not str_category_code:
        return None
    for _category in game_category_names:
        if _category['code'] == str_category_code:
            _name = _category['display']
            return _name
    return None


def already_alert_warning_no_data(_driver):
    _warning_elems = _driver.find_elements_by_class_name('alert-warning')
    if not _warning_elems:
        return False
    for _warning_elem in _warning_elems:
        if hasattr(_warning_elem, 'tag_name'):
            _warning_elem_tag_name = _warning_elem.tag_name
            if 'p' == _warning_elem_tag_name and hasattr(_warning_elem, 'text'):
                _text = _warning_elem.text.strip()
                if _text:
                    if 'There is no ranking data available on this date' \
                       ', for the selected country and category.' == _text:
                        return True
    return False


def ios_feed_to_order_by(feed):
    if IOSFeedType.FEED_FREE == feed:
        return IOSTopChartOrderBy.RANK_FREE
    elif IOSFeedType.FEED_PAID == feed:
        return IOSTopChartOrderBy.RANK_PAID
    elif IOSFeedType.FEED_GROSSING == feed:
        return IOSTopChartOrderBy.RANK_GROSSING
    else:
        return None


def android_feed_to_order_by(feed):
    if feed == AndroidFeedType.FEED_FREE:
        return AndroidTopChartOrderBy.RANK_FREE
    elif feed == AndroidFeedType.FEED_NEW_FREE:
        return AndroidTopChartOrderBy.RANK_NEW_FREE
    elif feed == AndroidFeedType.FEED_GROSSING:
        return AndroidTopChartOrderBy.RANK_GROSSING
    elif feed == AndroidFeedType.FEED_PAID:
        return AndroidTopChartOrderBy.RANK_PAID
    elif feed == AndroidFeedType.FEED_NEW_PAID:
        return AndroidTopChartOrderBy.RANK_NEW_PAID
    else:
        return None


def get_now_ymdhms_str():
    _now_str_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d%H%M%S')
    return _now_str_time


def standard_https_store_url(store_url):
    if not store_url:
        return None
    store_url = parse.unquote(store_url)
    _elems = parse.urlparse(store_url)
    if 'play.google.com' in store_url:
        store_url = 'https://' + _elems.netloc + _elems.path + '?' + _elems.query
    elif 'itunes.apple.com' in store_url:
        # store_url = 'https://' + _elems.netloc + _elems.path
        store_url = 'https://itunes.apple.com' + standard_ios_store_url_path(_elems.path)
    return store_url


def standard_ios_store_url_path(path):
    result = re.findall('/id\d*', path)
    if result:
        if result[0]:
            if '/app/' in path:
                return '/app' + result[0]
            elif '/app-bundle/' in path:
                return '/app-bundle' + result[0]
    else:
        return ''


def get_utc_to_machine_offset_hours():
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    offset_hours = offset / 60 / 60 * -1
    return int(offset_hours)


def get_hour_delta():
    utc_to_cst_offset_hours = +8
    utc_to_machine_offset_hours = get_utc_to_machine_offset_hours()
    hour_delta = utc_to_cst_offset_hours - utc_to_machine_offset_hours
    return hour_delta


def get_cst_yesterday():
    """ get China Standard Time yesterday """
    hour_delta = get_hour_delta()
    cst_time = datetime.now() + timedelta(hours=hour_delta)
    cst_time = cst_time + timedelta(days=-1)
    cst_time_str = cst_time.strftime('%Y-%m-%d')
    return cst_time_str


def get_cst_to_machine_hour_and_minute(h_m):
    tmp_time = datetime.strptime(h_m, '%H:%M')
    hour_delta = get_hour_delta()
    tmp_time = tmp_time - timedelta(hours=hour_delta)
    ret = tmp_time.strftime('%H:%M')
    return ret

