# -*- coding:utf-8 -*-
import time
import traceback
import re
from retry import retry
from selenium.common.exceptions import NoSuchElementException

import settings as _s
from appannieenum import AppRankingDBField, OSType, TopAppDBField, AccountStatus, AppannieCountry
from commonutils import standard_https_store_url, asking_me_areyouhuman, is_on_error_page, \
    get_now_ymdhms_str, app_has_been_removed, oops_account_has_been_blocked, oops_request_problem_occurred
from driverofselenium import ImageLessDriver
from loggers import get_logger
from managercookies import CookiesShuffler


class AppStoreUrlCrawler:
    def __init__(self, country=AppannieCountry.UNITED_STATE, os_type=OSType.IOS):
        self._driver = None
        self._ios_app_detail_url_template = 'https://www.appannie.com/apps/ios/app/%s/details/'
        self._android_app_detail_url_template = 'https://www.appannie.com/apps/google-play/app/%s/details/'
        self._csr = CookiesShuffler(country)
        self._first_crawl = True
        self._os_type = os_type

    def crawl_store_url(self, record, interval_func=None):
        if _s.enable_offline_concat_app_store_url and OSType.Android == self._os_type:
            return self._concat_android_store_url(record)
        if not self._driver:
            self._driver = ImageLessDriver(_s.default_crawl_mode)
        _driver = self._driver
        _detail_url = self._get_appannie_app_detail_url(record[TopAppDBField.FIELD_DETAIL_ID])
        if self._first_crawl:
            _driver.load_cookies(self._csr.shuffle().deal())
            self._first_crawl = False
        else:
            _driver.load_cookies(self._csr.deal(), None)
        get_logger().info('crawling store url of [%s: %s]' % (record[AppRankingDBField.FIELD_RANKING],
                                                              record[TopAppDBField.FIELD_APP_ID]))
        _app_url = None
        try:
            _app_url = self._retryable_crawl_target_xpath_(_detail_url)
        except NoSuchElementException as e:
            _account_status = None
            if asking_me_areyouhuman(_driver()):
                _account_status = AccountStatus.NEED_CAPTCHA
            elif is_on_error_page(_driver()):
                if oops_request_problem_occurred(_driver()):
                    _account_status = AccountStatus.NORMAL
                    get_logger().info('There was a problem processing request.')
                elif oops_account_has_been_blocked(_driver()):
                    _account_status = AccountStatus.BLOCKED
            if _account_status and _account_status != AccountStatus.NORMAL:
                _now_str_time = get_now_ymdhms_str()
                _screenshot_file = '%s-%s-%s.png' % (self._csr.get_current_account()['email'],
                                                     _account_status.name, _now_str_time)
                _screenshot_file = _driver.take_screenshot(file_name=_screenshot_file)
                _cookies = self._csr.discard(remove_from_account_list=True,
                                             send_mail_with_account_status=_account_status,
                                             screenshot_file=_screenshot_file).shuffle().deal()
                get_logger().error('Error crawl %s detail page:' % record[TopAppDBField.FIELD_APP_ID])
                get_logger().error('Account is on abnormal status: %s' % _account_status.name)
            elif app_has_been_removed(_driver()):
                get_logger().info(
                    'This app has been removed from the store: %s' % record[TopAppDBField.FIELD_APP_ID])
            else:
                #_app_url = self._get_store_url_by_page_source()
                if not _app_url:
                    get_logger().error('Error crawl %s detail page:' % record[TopAppDBField.FIELD_APP_ID])
                    get_logger().error('Traceback:\n%s' % traceback.format_exc())
        if _app_url:
            _app_url = standard_https_store_url(_app_url)
            get_logger().info('acquire: %s' % _app_url)
        if interval_func:
            interval_func()
        return _app_url

    @retry(NoSuchElementException, tries=3, delay=2)
    def _retryable_crawl_target_xpath_(self, _detail_url):
        #get_logger().info(_detail_url)
        self._driver().get(_detail_url)
        time.sleep(1)
        _app_url = None
        _elem = self._driver().find_element_by_xpath(_s.appannie_detail_page_store_elem)
        _app_url = _elem.get_attribute('app-confirm')
        if not _app_url:
            _elem = self._driver().find_element_by_xpath(_s.appannie_detail_page_store_elem_2)
            _app_url = _elem.get_attribute('app-confirm')
        return _app_url

    def _get_appannie_app_detail_url(self, appannie_app_id):
        if self._os_type == OSType.IOS:
            return self._ios_app_detail_url_template % appannie_app_id
        else:
            return self._android_app_detail_url_template % appannie_app_id

    def _get_store_url_by_page_source(self):
        sr = self._driver().page_source
        if sr:
            url_list = None
            if self._os_type == OSType.IOS:
                url_list = re.findall('https://itunes.apple.com/app[^"\']*', sr, re.S)
            elif self._os_type == OSType.Android:
                url_list = re.findall('https://play.google.com/store/apps/details[^"\']*', sr, re.S)
            if url_list:
                url_set = set(url_list)
                if len(url_set) == 1:
                    url = url_set.pop()
                    get_logger().info('get_store_url_by_page_source: [%s]' % url)
                    return url
        return None

    @staticmethod
    def _concat_android_store_url(record):
        tmp = 'https://play.google.com/store/apps/details?id=' + record[TopAppDBField.FIELD_APP_ID]
        get_logger().info('concat [%s: %s] store url: %s' % (
            record[AppRankingDBField.FIELD_RANKING], record[AppRankingDBField.FIELD_APP_ID], tmp))
        return tmp

    def open_conn(self):
        return self

    def close_conn(self):
        if self._driver:
            self._driver().quit()


if __name__ == '__main__':
    """"""
