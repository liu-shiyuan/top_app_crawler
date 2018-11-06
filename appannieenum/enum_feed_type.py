# -*- coding:utf-8 -*-


class IOSFeedType:
    FEED_ALL = 'All'
    FEED_FREE = 'Free'
    FEED_PAID = 'Paid'
    FEED_GROSSING = 'Grossing'


class AndroidFeedType:
    FEED_ALL = 'All'
    FEED_FREE = 'Free'
    FEED_PAID = 'Paid'
    FEED_GROSSING = 'Grossing'
    FEED_NEW_FREE = 'New-Free'
    FEED_NEW_PAID = 'New-Paid'


if __name__ == '__main__':
    print(AndroidFeedType.FEED_GROSSING)
