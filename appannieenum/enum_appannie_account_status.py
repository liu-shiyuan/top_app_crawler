# -*- coding:utf-8 -*-
from enum import Enum


class AccountStatus(Enum):
    UNKNOWN = 0
    NORMAL = 1
    NEED_CAPTCHA = 2
    BLOCKED = 3


if __name__ == '__main__':
    print(AccountStatus.BLOCKED.name)
