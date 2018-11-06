# -*- coding:utf-8 -*-
from loggers import get_logger
from db import IconIdDeterminer
from datetime import datetime, timedelta
import settings as _s
import re
from commonutils.util_fun import get_category_display_name
from appannieenum import AppRankingDBField, TopAppDBField
import pytz


class TopListParser:
    def __init__(self, bs, country, query_date, feed_type, sub_category_code):
        self.bs = bs
        self.country = country
        self.query_date = query_date
        self.feed_type = feed_type
        self.sub_category = get_category_display_name(sub_category_code)
        self.my_date_format = '%Y-%m-%d %H:%M:%S'
        self.result_set = None
        self.target_table = None
        self.appannie_crawl_date = None
        self.column_index_map = None
        self.target_trs = None

    def parse(self):
        get_logger().info('parsing feed type: %s...' % self.feed_type)
        self.get_target_table()
        self.get_column_index_map()
        self.get_table_trs()
        self.get_appannie_crawl_date()
        _result_set = []
        _result = None
        ider = None
        try:
            ider = IconIdDeterminer()
            ider.open_conn()
            for every_tr in self.target_trs:
                _target_tds = self.get_target_row(every_tr)
                _result = self.get_parse_record_result(_target_tds)
                _result = self.handle_normal_fields(_result, ider)
                _result = self.handle_extra_fields(_result)
                _result_set.append(_result)
            self.result_set = _result_set
        finally:
            if ider:
                ider.close_conn()
        return self.result_set

    def get_parse_record_result(self, _target_tds):
        return []

    def get_target_table(self):
        _bs = self.bs
        _tables = _bs.findAll('table')
        _table1 = _tables[0]
        self.target_table = _table1
        return self.target_table

    def get_appannie_crawl_date(self):
        _bs = self.bs
        _appannie_date_format = '%b %d, %Y %I:%M%p'
        _my_date_format = '%Y-%m-%d'
        _crawl_date_span = _bs.find('span', attrs={'data-helptip': re.compile('.*'), 'class': 'ng-binding'})
        if _crawl_date_span:
            _raw_crawl_date = _crawl_date_span.string.strip()
            _crawl_date_s = _raw_crawl_date.split('\n')
            _crawl_date_str = _crawl_date_s[0]
            _crawl_date_tz = _crawl_date_s[1].strip()
            _delta = 8 - int(str(_crawl_date_tz[3:]))
            _crawl_date = datetime.strptime(_crawl_date_str, _appannie_date_format) + timedelta(hours=_delta)
            _crawl_date_ret = _crawl_date.strftime(_my_date_format)
            self.appannie_crawl_date = _crawl_date_ret
            return self.appannie_crawl_date

    def get_column_index_map(self):
        _table = self.target_table
        _theads = _table.findAll('thead')
        _thead = _theads[0]
        _thead_ths = _thead.findAll('th')
        _c_2_i_map = dict()
        for idx in list(range(len(_thead_ths))):
            _c_2_i_map[_thead_ths[idx].findChild('span').string] = idx
        self.column_index_map = _c_2_i_map
        return self.column_index_map

    def get_table_trs(self):
        _table = self.target_table
        _t_1_body = _table.findAll('tbody')[0]
        _trs = _t_1_body.find_all('tr')
        self.target_trs = _trs
        return self.target_trs

    @staticmethod
    def get_target_row(tr):
        tmp = []
        tr_tds = tr.findAll('td')
        for _td in tr_tds:
            if _s.ios_skip_column_with_class not in _td.attrs['class']:
                tmp.append(_td)
        return tmp

    def handle_normal_fields(self, _result, _ider):
        _result[AppRankingDBField.FIELD_APPANNIE_CRAWL_DATE] = self.appannie_crawl_date
        _result[AppRankingDBField.FIELD_UPDATE_TIME] = datetime.now(pytz.timezone('Asia/Shanghai')) \
            .strftime(self.my_date_format)
        _result[AppRankingDBField.FIELD_QUERY_DATE] = self.query_date
        _result[AppRankingDBField.FIELD_FEED_TYPE] = self.feed_type
        if _result[AppRankingDBField.FIELD_ICON_ID]:
            _result[AppRankingDBField.FIELD_ICON_ID] = _ider.get_icon_id(_result[AppRankingDBField.FIELD_ICON_ID])
        _result[AppRankingDBField.FIELD_COUNTRY] = self.country
        _result[AppRankingDBField.FIELD_QUERY_CATEGORY] = self.sub_category
        if not _result[AppRankingDBField.FIELD_CATEGORY]:
            _result[AppRankingDBField.FIELD_CATEGORY] = self.sub_category
        return _result

    @staticmethod
    def handle_extra_fields(_result):
        return _result


def get_detail_id(appannie_app_uri):
    """
    :param appannie_app_uri:
    :return: str: app_id
    example:
    input: /apps/ios/app/fortnite/details/
    output: fortnite
    """
    tmp = appannie_app_uri.split('/')
    if 'details' in tmp:
        return tmp[4]
    else:
        return None


def get_company_id(uri):
    """
    :param uri:
    :return: str: company_id
    example:
    input: /company/1000200000000041/
    output: 1000200000000041
    """
    tmp = uri.split('/')
    if 'company' in tmp:
        return tmp[2]
    else:
        return None


def get_publisher_id(uri):
    """
    :param uri:
    :return: str: publisher_id
    example:
    input: /apps/ios/publisher/431865278/
    output: 431865278
    """
    tmp = uri.split('/')
    if 'publisher' in tmp:
        return tmp[4]
    else:
        return None


class TopRecordParser:
    def __init__(self, tds, column_index_map, feed):
        self.tds = tds
        self.column_index_map = column_index_map
        self.feed_type = feed
        self.result = dict()
        self.my_date_format = '%Y-%m-%d'

    def parse(self):
        self.crawl_ranking()
        self.crawl_app_info()
        self.crawl_ranking_change()
        self.crawl_category()
        self.crawl_release_and_update_date()
        return self.result

    def crawl_ranking(self):
        # ranking
        ranking_str = self.tds[self.column_index_map[self.get_page_field_set().RANKING]].string
        self.result[AppRankingDBField.FIELD_RANKING] = int(ranking_str)

    def crawl_app_info(self):
        app_info_td = self.tds[self.column_index_map[self.get_page_field_set().APP_INFO]]
        data_app_id = app_info_td.attrs['data-appid']
        self.result[AppRankingDBField.FIELD_APP_ID] = data_app_id
        self.result[TopAppDBField.FIELD_UNIFIED_APP_ID] = data_app_id
        app_info_a_tags = app_info_td.findAll('a')
        for _a_tag in app_info_a_tags:
            if 'icon-link' in _a_tag.get('class'):
                _app_icon_uri = _a_tag.img.get('src')
                self.result[AppRankingDBField.FIELD_ICON_ID] = _app_icon_uri
                break
        for _a_tag in app_info_a_tags:
            if 'app-link' in _a_tag.attrs['class']:
                appannie_app_uri = _a_tag.attrs['href']
                detail_id = get_detail_id(appannie_app_uri)
                self.result[TopAppDBField.FIELD_DETAIL_ID] = detail_id
                app_name = _a_tag.span.string
                self.result[AppRankingDBField.FIELD_APP_NAME] = app_name
                break
        for _a_tag in app_info_a_tags:
            if 'company-link' in _a_tag.attrs['class']:
                appannie_develop_uri = _a_tag.attrs['href']
                company_id = get_company_id(appannie_develop_uri)
                publisher_id = get_publisher_id(appannie_develop_uri)
                owner_name = _a_tag.span.string
                self.result[TopAppDBField.FIELD_COMPANY_ID] = company_id
                self.result[TopAppDBField.FIELD_PUBLISHER_ID] = publisher_id
                self.result[TopAppDBField.FIELD_OWNER_NAME] = owner_name
                break
        self.result[AppRankingDBField.FIELD_HAS_IAP] = 0
        app_info_span_tags = self.tds[self.column_index_map[self.get_page_field_set().APP_INFO]].findAll('span')
        for _span_tag in app_info_span_tags:
            if _span_tag.get('class') and 'iap-info' in _span_tag.get('class'):
                self.result[AppRankingDBField.FIELD_HAS_IAP] = 1
                break

    def crawl_ranking_change(self):
        _target_ranking_change_column = self.get_target_ranking_change_column(self.feed_type)
        _change_str = self.tds[self.column_index_map[_target_ranking_change_column]].string
        _ranking_change_claz = self.tds[self.column_index_map[_target_ranking_change_column]].span.get('class')
        if 'same' in _ranking_change_claz:
            self.result[AppRankingDBField.FIELD_RANKING_CHANGE] = 0
        else:
            _change_str = re.findall('\d+', _change_str.strip())
            if not _change_str:
                self.result[AppRankingDBField.FIELD_RANKING_CHANGE] = 0
            else:
                _change_number = int(_change_str[0])
                if 'green' in _ranking_change_claz:
                    self.result[AppRankingDBField.FIELD_RANKING_CHANGE] = _change_number
                elif 'red' in _ranking_change_claz:
                    self.result[AppRankingDBField.FIELD_RANKING_CHANGE] = -_change_number

    def crawl_category(self):
        self.result[AppRankingDBField.FIELD_CATEGORY] = self.tds[
            self.column_index_map[self.get_page_field_set().SUB_CATEGORY]].string

    def crawl_release_and_update_date(self):
        appannie_date_format = '%b %d, %Y'
        r_d_str = self.tds[self.column_index_map[self.get_page_field_set().RELEASE_DATE]].span.string
        l_u_str = self.tds[self.column_index_map[self.get_page_field_set().LAST_UPDATE_DATE]].span.string
        if 'N/A' != r_d_str:
            r_d_str = datetime.strptime(r_d_str, appannie_date_format).strftime(self.my_date_format)
        if 'N/A' != l_u_str:
            l_u_str = datetime.strptime(l_u_str, appannie_date_format).strftime(self.my_date_format)
        self.result[TopAppDBField.FIELD_RELEASE_DATE] = r_d_str
        self.result[TopAppDBField.FIELD_LAST_UPDATE_DATE] = l_u_str

    @staticmethod
    def get_target_ranking_change_column(feed):
        return ''

    # @staticmethod
    # def get_db_field_set():
    #     return None

    @staticmethod
    def get_page_field_set():
        return None
