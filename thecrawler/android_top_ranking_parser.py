# -*- coding:utf-8 -*-
from thecrawler.top_ranking_parser import TopListParser, TopRecordParser
from appannieenum import AndroidTopColumn, AndroidFeedType, AppRankingDBField, OSType, AndroidGameCategory, \
    TopAppDBField
from bs4 import BeautifulSoup as Bs


class AndroidTopListParser(TopListParser):
    def __init__(self, bs, country, query_date, feed_type, sub_category_code):
        super().__init__(bs, country, query_date, feed_type, sub_category_code)

    def get_parse_record_result(self, _target_tds):
        _result = AndroidTopRecordParser(tds=_target_tds, column_index_map=self.column_index_map,
                                         feed=self.feed_type).parse()
        return _result

    @staticmethod
    def handle_extra_fields(record):
        record[AppRankingDBField.FIELD_OS] = OSType.Android
        if record[TopAppDBField.FIELD_DETAIL_ID]:
            record[AppRankingDBField.FIELD_APP_ID] = record[TopAppDBField.FIELD_DETAIL_ID]
        return record


class AndroidTopRecordParser(TopRecordParser):
    def __init__(self, tds, column_index_map, feed):
        super().__init__(tds, column_index_map, feed)

    @staticmethod
    def get_target_ranking_change_column(feed):
        if AndroidFeedType.FEED_FREE == feed:
            return AndroidTopColumn.RANKING_CHANGE_FREE
        elif AndroidFeedType.FEED_PAID == feed:
            return AndroidTopColumn.RANKING_CHANGE_PAID
        elif AndroidFeedType.FEED_GROSSING == feed:
            return AndroidTopColumn.RANKING_CHANGE_GROSSING
        elif AndroidFeedType.FEED_NEW_FREE == feed:
            return AndroidTopColumn.RANKING_CHANGE_NEW_FREE
        elif AndroidFeedType.FEED_NEW_PAID == feed:
            return AndroidTopColumn.RANKING_CHANGE_NEW_PAID
        else:
            return None

    @staticmethod
    def get_page_field_set():
        return AndroidTopColumn


if __name__ == '__main__':
    _main_bs = Bs(open('../data/android_Card_Free_top.html', encoding='utf-8'), 'lxml')
    _main_result = AndroidTopListParser(bs=_main_bs, country='US', query_date='2018-09-16',
                                        feed_type=AndroidFeedType.FEED_FREE,
                                        sub_category_code=AndroidGameCategory.CATEGORY_CARD).parse()
    print(_main_result)
