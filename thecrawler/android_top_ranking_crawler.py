# -*- coding:utf-8 -*-
from commonutils import AndroidTopChartUrlBuilder
from thecrawler.top_ranking_crawler import TopListCrawler
from appannieenum import AppannieCountry, AndroidGameCategory, AndroidFeedType, AndroidTopChartOrderBy, CrawlerMode


class AndroidTopListCrawler(TopListCrawler):
    def __init__(self, country, sub_category_code, feed_type, order_by, query_date=None, mode=CrawlerMode.Runtime):
        super().__init__(country, sub_category_code, feed_type, query_date, mode)
        self._country = country
        self._order_by = order_by
        self._query_date = query_date
        self._sub_category_code = sub_category_code
        self._feed_type = feed_type

    def get_dest_url(self):
        _builder = AndroidTopChartUrlBuilder() \
            .with_country(self._country) \
            .with_sub_category(self._sub_category_code) \
            .with_feed(self._feed_type) \
            .with_order_by(self._order_by)
        if self._query_date:
            _builder.with_date(self._query_date)
        else:
            _builder.with_yesterday()
        _url = _builder.get_i18n_en_url()
        return _url

    def get_os_type(self):
        return 'android'


if __name__ == '__main__':
    AndroidTopListCrawler(AppannieCountry.UNITED_STATE, AndroidGameCategory.CATEGORY_CARD, AndroidFeedType.FEED_FREE,
                          AndroidTopChartOrderBy.RANK_FREE, query_date='2018-09-16', mode=CrawlerMode.Debug).crawl()
