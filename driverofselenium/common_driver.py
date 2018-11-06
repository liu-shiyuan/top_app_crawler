# -*- coding:utf-8 -*-
import os
from selenium import webdriver
import settings as _s
from appannieenum import CrawlerMode


class CommonDriver:
    def __init__(self, mode=CrawlerMode.Runtime, need_proxy=_s.need_proxy):
        self._mode = mode
        self._need_proxy = need_proxy
        options = self.__get_chrome_options__()
        self._driver = webdriver.Chrome(executable_path=_s.chrome_driver_path, chrome_options=options)
        self._driver.set_window_size(1200, 900)

    def __get_chrome_prefs__(self):
        prefs = dict()
        # disable popups
        prefs['profile.default_content_settings.popups'] = 0
        return prefs

    def __get_chrome_options__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--lang=en-US')
        options.add_argument('--disable-plugins-discovery')
        options.add_argument('--disable-component-update')
        # options.add_argument('screenshot')
        # options.add_argument('window-size=1200,900')
        prefs = self.__get_chrome_prefs__()
        options.add_experimental_option('prefs', prefs)
        if self._mode is CrawlerMode.Runtime:
            options.add_argument('--headless')
            if not self._need_proxy:
                options.add_argument("--proxy-server='direct://'")
                options.add_argument("--proxy-bypass-list=*")
        if self._need_proxy:
            options.add_argument("--proxy-server='%s:%s'" % (_s.proxy_host, _s.proxy_port))
        return options

    def get_driver(self):
        return self._driver

    def close(self):
        self._driver.quit()

    def __call__(self):
        return self.get_driver()

    def load_cookies(self, list_cookies, first_to_url=_s.appannie_login_referer_url):
        if first_to_url:
            self.get_driver().get(first_to_url)
        self.get_driver().delete_all_cookies()
        for cookie in list_cookies:
            self.get_driver().add_cookie(cookie)
        return self.get_driver()

    def take_screenshot(self, file_name, save_path=_s.default_screenshot_dir):
        _screenshot_file = os.path.join(save_path, file_name)
        self._driver.save_screenshot(_screenshot_file)
        return _screenshot_file


class ImageLessDriver(CommonDriver):
    def __init__(self, mode=CrawlerMode.Runtime):
        super().__init__(mode)

    def __get_chrome_prefs__(self):
        _prefs = super().__get_chrome_prefs__()
        _prefs['profile.managed_default_content_settings.images'] = 2
        _prefs['profile.default_content_settings.images'] = 2
        return _prefs
