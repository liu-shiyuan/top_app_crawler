# -*- coding:utf-8 -*-
import json
import time
from datetime import datetime, timedelta
import settings as _s
from driverofselenium import ImageLessDriver
from loggers import get_logger
import os
import random
import copy
from mailalert import sent_alert_to_receivers, sent_alert_to_receivers_with_screenshot
from crawlexception import NoAccountException
from manageraccounts import load_accounts, remove_appannie_account
from appannieenum import AppannieCountry
from managercookies.account_proxy import SimpleCountryLevelAccountProxy as SCLAProxy


class CookiesGenerator:
    def __init__(self, no, email, pwd, country):
        self._no = no
        self._email = email
        self._pwd = pwd
        self._country = country
        self._json_file_path = self._get_json_file_full_path_()

    def generate(self):
        dict_cookies = None
        _driver = None
        try:
            _driver = ImageLessDriver(mode=_s.default_crawl_mode)
            _driver().get(_s.appannie_login_referer_url)
            email_element = _driver().find_element_by_id('email')
            pwd_element = _driver().find_element_by_id('password')
            submit_button_element = _driver().find_element_by_id('submit')
            email_element.send_keys(self._email)
            time.sleep(1)
            pwd_element.send_keys(self._pwd)
            time.sleep(1)
            submit_button_element.click()
            time.sleep(1)
            dict_cookies = _driver().get_cookies()
            json_cookies = json.dumps(dict_cookies)
            json_file = self._json_file_path
            with open(json_file, 'w', encoding='utf-8') as f:
                f.write(json_cookies)
            time.sleep(1)
            get_logger().info('renew %s: %s cookies succeeded' % (self._no, self._email))
        finally:
            if _driver:
                _driver().quit()
        return dict_cookies

    def _get_json_file_full_path_(self):
        return _s.default_cookies_dir + str.lower(self._country) + '.' + self._no + _s.cookies_json_file_suffix

    def get_valid_cookies(self):
        if not os.path.isfile(self._json_file_path):
            return self.generate()
        elif self._whether_exceed_durable_days():
            return self.generate()
        else:
            with open(self._json_file_path, 'r', encoding='utf-8') as f:
                list_cookies = json.loads(f.read())
                if not list_cookies:
                    return self.generate()
                return list_cookies

    def _whether_exceed_durable_days(self):
        file_modified_timestamp = os.stat(self._json_file_path).st_mtime
        cookies_generate_deadline = datetime.now() + timedelta(days=-_s.cookies_durable_days)
        deadline_timestamp = time.mktime(cookies_generate_deadline.timetuple())
        return file_modified_timestamp < deadline_timestamp


class CookiesShuffler:
    def __init__(self, country=AppannieCountry.UNITED_STATE):
        #self._country = country
        self._country = SCLAProxy(country).get_country()
        self._accounts = self._get_account_list(self._country)
        if self._accounts:
            self._next_account = self._accounts[0]
            self._account_len = len(self._accounts)
        else:
            self._next_account = None
            self._account_len = 0
        self._current_account = self._next_account

    def deal(self):
        if not (self._accounts and self._next_account):
            raise NoAccountException('No useful account to crawl')
        self._current_account = self._next_account
        _current_cookies = CookiesGenerator(self._current_account['no'], self._current_account['email'],
                                            self._current_account['pwd'], self._country).get_valid_cookies()
        get_logger().info('using account %s %s: %s to crawl..' %
                          (self._country, self._current_account['no'], self._current_account['email']))
        for index in range(0, self._account_len):
            if self._current_account['no'] == self._accounts[index]['no']:
                self._next_account = self._accounts[(index + 1) % self._account_len]
                break
        return _current_cookies

    @staticmethod
    def _get_account_list(country):
        with load_accounts(country) as accounts:
            _accounts = copy.deepcopy(accounts)
            return _accounts

    def get_current_account(self):
        tmp = dict()
        tmp['no'] = self._current_account['no']
        tmp['email'] = self._current_account['email']
        return tmp

    def discard(self, remove_from_account_list=False, send_mail_with_account_status=None, screenshot_file=None):
        get_logger().info('discarding account: %s' % self._current_account['email'])
        if not (self._accounts and self._current_account):
            raise NoAccountException('No account to discard')
        for index in range(0, self._account_len):
            if self._current_account['no'] == self._accounts[index]['no']:
                del self._accounts[index]
                self._account_len = len(self._accounts)
                break
        if remove_from_account_list:
            remove_appannie_account(self._country, self._current_account)
            if send_mail_with_account_status:
                if screenshot_file:
                    sent_alert_to_receivers_with_screenshot(country=self._country,
                                                            account_info=self._current_account,
                                                            account_status=send_mail_with_account_status,
                                                            screenshot_file=screenshot_file)
                else:
                    sent_alert_to_receivers(country=self._country,
                                            account_info=self._current_account,
                                            account_status=send_mail_with_account_status)
        return self

    def shuffle(self):
        if self._accounts:
            random.shuffle(self._accounts)
            self._next_account = self._accounts[0]
        else:
            raise NoAccountException('No account to shuffle')
        return self


if __name__ == '__main__':
    # main_cookies = CookiesShuffler().shuffle().deal()
    # print(main_cookies)
    cc = CookiesShuffler(AppannieCountry.UNITED_STATE)
    for i in range(0, 15):
        cc.deal()
        print(cc.get_current_account()['no'])

        if cc.get_current_account()['no'] in ['3']:
            cc.discard()
        if i == 5:
            cc.shuffle()
        if i >= 8:
            cc.discard()
