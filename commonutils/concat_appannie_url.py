# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from urllib import parse as url_parser
import pytz
from appannieenum import AndroidGameCategory, IOSGameCategory, AppannieCountry, AndroidFeedType, IOSFeedType, \
    AndroidTopChartOrderBy, IOSTopChartOrderBy
import settings as _s


class BaseAppannieUrlBuilder:
    def __init__(self):
        self._protocol = 'https'
        self._domain = 'www.appannie.com'
        self._rank_sorting_type = 'rank'
        self._page_number = 0
        self._page_size = 500
        self._table_selections = ''
        self._order_type = 'desc'
        self._order_by = 'free_rank'
        self._uri = None
        self._device = None

        self._country = None
        self._sub_category_code = None
        self._date_str = None
        self._feed = None

    def __get_query_string__(self):
        _q_s = dict()
        if self._country is not None:
            _q_s['country'] = self._country
        if self._sub_category_code is not None:
            _q_s['category'] = self._sub_category_code
        if self._device is not None:
            _q_s['device'] = self._device
        if self._date_str is not None:
            _q_s['date'] = self._date_str
        if self._feed is not None:
            _q_s['feed'] = self._feed
        if self._rank_sorting_type is not None:
            _q_s['rank_sorting_type'] = self._rank_sorting_type
        if self._page_number is not None:
            _q_s['page_number'] = self._page_number
        if self._page_size is not None:
            _q_s['page_size'] = self._page_size
        if self._table_selections is not None:
            _q_s['table_selections'] = self._table_selections
        if self._order_type is not None:
            _q_s['order_type'] = self._order_type
        if self._order_by is not None:
            _q_s['order_by'] = self._order_by
        _query_str = url_parser.urlencode(_q_s)
        return _query_str

    def get_url(self):
        _q_s = self.__get_query_string__()
        _url = url_parser.urlunparse((self._protocol, self._domain, self._uri, None, _q_s, None))
        return _url

    def get_i18n_en_url(self):
        """
        https://www.appannie.com/i18n/activate/cn/?next=%2Fapps%2Fios%2Ftop-chart%2F%3Fcountry%3DUS%26category%3D7003%26device%3Diphone%26date%3D2018-09-02%26feed%3DFree%26rank_sorting_type%3Drank%26page_number%3D0%26page_size%3D100%26table_selections%3D%26metrics%3Dgrossing_rank%2Ccategory%2Call_avg%2Call_count%2Clast_avg%2Clast_count%2Cfirst_release_date%2Clast_updated_date%2Cest_download%2Cest_revenue%2Cwau%26order_type%3Ddesc%26order_by%3Dfree_rank
        /apps/ios/top-chart/?country=US&category=7003&device=iphone&date=2018-09-02&feed=Free&rank_sorting_type=rank&page_number=0&page_size=100&table_selections=&metrics=grossing_rank,category,all_avg,all_count,last_avg,last_count,first_release_date,last_updated_date,est_download,est_revenue,wau&order_type=desc&order_by=free_rank
        """
        _url = self.get_url()
        _target_url = _url[_url.find(self._domain) + len(self._domain):]
        _encoded_target_url = url_parser.quote(_target_url)
        _i18n_en_url = _s.appannie_i18n_us_redirect_url + _encoded_target_url
        return _i18n_en_url

    def with_country(self, country):
        self._country = country
        return self

    def with_sub_category(self, c):
        self._sub_category_code = c
        return self

    def with_date(self, d):
        self._date_str = d
        return self

    def with_feed(self, feed):
        self._feed = feed
        return self

    def with_order_by(self, field):
        self._order_by = field
        return self

    def with_yesterday(self):
        _cntz = pytz.timezone('Asia/Shanghai')
        _yesterday = datetime.now(_cntz) + timedelta(days=-1)
        self._date_str = _yesterday.strftime('%Y-%m-%d')
        return self


class IOSTopChartUrlBuilder(BaseAppannieUrlBuilder):
    def __init__(self):
        super().__init__()
        self._uri = 'apps/ios/top-chart'
        self._device = 'iphone'


class AndroidTopChartUrlBuilder(BaseAppannieUrlBuilder):
    def __init__(self):
        super().__init__()
        self._uri = 'apps/google-play/top-chart'
        self._device = ''


if __name__ == '__main__':
    query_str = AndroidTopChartUrlBuilder().__get_query_string__()
    print(query_str)
    url = AndroidTopChartUrlBuilder()\
        .with_sub_category(AndroidGameCategory.CATEGORY_CARD)\
        .with_country(AppannieCountry.UNITED_STATE)\
        .with_feed(AndroidFeedType.FEED_GROSSING)\
        .with_order_by(AndroidTopChartOrderBy.RANK_FREE) \
        .with_date('2018-08-27') \
        .get_i18n_en_url()  # .get_url()
    print(url)
    url = IOSTopChartUrlBuilder()\
        .with_sub_category(IOSGameCategory.CATEGORY_CARD)\
        .with_country(AppannieCountry.JAPAN)\
        .with_feed(IOSFeedType.FEED_FREE)\
        .with_order_by(IOSTopChartOrderBy.RANK_PAID) \
        .with_yesterday() \
        .get_url()
    print(url)
