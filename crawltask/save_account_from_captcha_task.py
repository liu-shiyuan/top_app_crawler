# -*- coding:utf-8 -*-
import settings as _s
from driverofselenium import CommonDriver
import json
from appannieenum import CrawlerMode, AppannieCountry


_target_user_No = 8
_target_country = AppannieCountry.SINGAPORE


def _do_areyouhuman_test(user_No, country):
    _driver = CommonDriver(mode=CrawlerMode.Debug)
    _user_cookies_file = '%s%s.%s.cookies.json' % (_s.default_cookies_dir, str.lower(country), str(user_No))
    with open(_user_cookies_file, 'r', encoding='utf-8') as f:
        list_cookies = json.loads(f.read())
        _driver.load_cookies(list_cookies)
        return _driver()


if __name__ == '__main__':
    driver = _do_areyouhuman_test(user_No=_target_user_No, country=_target_country)
    _test_url = 'https://www.appannie.com/areyouhuman/?return_to=/dashboard/home/%3F_ref%3Dheader'
    # _test_url = 'https://www.appannie.com/dashboard/home/'
    driver.get(_test_url)
    #  need human guy to do the rest...
