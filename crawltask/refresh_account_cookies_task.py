# -*- coding:utf-8 -*-
from managercookies import CookiesGenerator
from appannieenum import AppannieCountry
from manageraccounts import load_accounts

_target_user_No = 10
_target_account_country = AppannieCountry.UNITED_STATE


def _do_task(current_account):
    _current_cookies = CookiesGenerator(current_account['no'], current_account['email'],
                                        current_account['pwd'], _target_account_country).generate()
    return _current_cookies


if __name__ == '__main__':
    with load_accounts(_target_account_country) as _accounts:
        if _accounts:
            for _account in _accounts:
                if _account['no'] == str(_target_user_No):
                    _new_cookies = _do_task(_account)
                    print(_new_cookies)
                    break
    print('refresh account cookies task done.')
