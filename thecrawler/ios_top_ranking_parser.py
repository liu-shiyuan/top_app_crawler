# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as Bs
from appannieenum import IOSTopColumn, IOSFeedType, IOSGameCategory, AppRankingDBField, OSType
from thecrawler.top_ranking_parser import TopListParser, TopRecordParser


class IosTopListParser(TopListParser):
    def __init__(self, bs, country, query_date, feed_type, sub_category_code):
        super().__init__(bs, country, query_date, feed_type, sub_category_code)

    def get_parse_record_result(self, _target_tds):
        _result = IosTopRecordParser(tds=_target_tds, column_index_map=self.column_index_map,
                                     feed=self.feed_type).parse()
        return _result

    @staticmethod
    def handle_extra_fields(record):
        record[AppRankingDBField.FIELD_OS] = OSType.IOS
        return record


class IosTopRecordParser(TopRecordParser):
    def __init__(self, tds, column_index_map, feed):
        super().__init__(tds, column_index_map, feed)

    @staticmethod
    def get_target_ranking_change_column(feed):
        if IOSFeedType.FEED_FREE == feed:
            return IOSTopColumn.RANKING_CHANGE_FREE
        elif IOSFeedType.FEED_PAID == feed:
            return IOSTopColumn.RANKING_CHANGE_PAID
        elif IOSFeedType.FEED_GROSSING == feed:
            return IOSTopColumn.RANKING_CHANGE_GROSSING
        else:
            return None

    @staticmethod
    def get_page_field_set():
        return IOSTopColumn



if __name__ == '__main__':
    _main_bs = Bs(open('../data/ios_Action_Free_top.html', encoding='utf-8'), 'lxml')
    _main_result = IosTopListParser(bs=_main_bs, country='US', query_date='2018-09-20', feed_type=IOSFeedType.FEED_FREE,
                                    sub_category_code=IOSGameCategory.CATEGORY_ACTION).parse()
    print(_main_result)
