# -*- coding:utf-8 -*-
from driverofselenium import ImageLessDriver
from commonutils import get_category_display_name, time_limit, get_now_ymdhms_str, already_alert_warning_no_data, \
    asking_me_areyouhuman, is_on_error_page, get_cst_yesterday, oops_account_has_been_blocked, oops_request_problem_occurred
from appannieenum import AccountStatus, CrawlerMode
import settings as _s
from managercookies import CookiesShuffler
import time
from loggers import get_logger


class TopListCrawler:
    def __init__(self, country, sub_category_code, feed_type, query_date, mode=CrawlerMode.Runtime):
        self._country = country
        self._sub_category_code = sub_category_code
        self._feed_type = feed_type
        self._query_date = query_date
        self._mode = mode
        self._driver = None
        self._formatted_category_display_name = None

    def _get_crawler_driver(self):
        _driver = ImageLessDriver(self._mode)
        return _driver

    def crawl(self):
        self._driver = self._get_crawler_driver()
        _category_display_name = get_category_display_name(self._sub_category_code)
        self._formatted_category_display_name = _category_display_name.replace(' ', '_')
        _ret_file_name = '%s_%s_%s_top.html' % (self.get_os_type(), self._formatted_category_display_name,
                                                self._feed_type)
        try:
            _url = self.get_dest_url()
            crawl_date = None
            if self._query_date:
                crawl_date = self._query_date
            else:
                crawl_date = get_cst_yesterday()
            timeout_msg = crawl_date + ' ' + self._country + ' ' + _ret_file_name
            with time_limit(_s.top_charts_page_crawler_time_out, 'timeout while crawling: %s' % timeout_msg):
                _is_success = self._do_crawl(_url)
            if _is_success:
                with open(_s.default_data_store_dir + _ret_file_name, 'w', encoding='utf-8') as f:
                    source = self._driver().page_source
                    f.write(source)
                return _ret_file_name
            else:
                return 'not_success'
        except Exception as e:
            _now_str_time = get_now_ymdhms_str()
            _screenshot_name = '%s_%s_%s_%s_screenshot.png' % (self.get_os_type(), _now_str_time,
                                                               self._formatted_category_display_name, self._feed_type)
            self._driver.take_screenshot(_screenshot_name)
            raise e
        finally:
            if self._driver:
                self._driver().quit()

    def get_dest_url(self):
        return ''

    def _do_crawl(self, dest_url):
        csr = CookiesShuffler(self._country)
        _cookies = csr.shuffle().deal()
        self._driver.load_cookies(_cookies).get(dest_url)
        table_elems = self._driver().find_elements_by_tag_name('table')
        while table_elems is None or len(table_elems) < 1:
            if already_alert_warning_no_data(self._driver()):
                get_logger().info('warning no data on [%s : %s] ' %
                                  (self._formatted_category_display_name, self._feed_type))
                return False
            else:
                _account_status = None
                if asking_me_areyouhuman(self._driver()):
                    _account_status = AccountStatus.NEED_CAPTCHA
                if is_on_error_page(self._driver()):
                    if oops_request_problem_occurred(self._driver()):
                        _account_status = AccountStatus.NORMAL
                        get_logger().info('There was a problem processing request.')
                    elif oops_account_has_been_blocked(self._driver()):
                        _account_status = AccountStatus.BLOCKED
                if _account_status and _account_status != AccountStatus.NORMAL:
                    csr.discard(remove_from_account_list=True, send_mail_with_account_status=_account_status)
                    _cookies = csr.deal()
                    self._driver.load_cookies(_cookies).get(dest_url)
            time.sleep(3)
            table_elems = self._driver().find_elements_by_tag_name('table')
        time.sleep(3)
        return True

    def get_os_type(self):
        return ''
