# -*- coding:utf-8 -*-
from appannieenum import AppannieCountry
from contextlib import contextmanager
from manageraccounts.accounts import *


@contextmanager
def load_accounts(country=AppannieCountry.UNITED_STATE):
    l_c = country.lower()
    accounts = eval(l_c + '_accounts')
    yield accounts


def remove_appannie_account(country, account):
    with load_accounts(country) as appannie_accounts:
        _count = len(appannie_accounts)
        for index in range(0, _count):
            if account['no'] == appannie_accounts[index]['no']:
                del appannie_accounts[index]
                break


def add_appannie_account(_account):
    #appannie_accounts.append(_account)
    pass