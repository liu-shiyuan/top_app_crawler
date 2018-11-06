# -*- coding:utf-8 -*-


# appannie page column name
class IOSTopColumn:
    RANKING = '#'
    APP_INFO = 'App'
    RANKING_CHANGE_FREE = 'Free Rank'
    RANKING_CHANGE_GROSSING = 'Grossing Rank'
    RANKING_CHANGE_PAID = 'Paid Rank'
    SUB_CATEGORY = 'Category'
    RELEASE_DATE = 'Release Date'
    LAST_UPDATE_DATE = 'Last Update'


class IOSTopDBFiled:
    FIELD_RANKING = 'ranking'
    FIELD_SUB_CATEGORY = 'sub_category'
    FIELD_RANKING_CHANGE = 'ranking_change'
    FIELD_APP_ID = 'appannie_app_id'
    FIELD_APP_NAME = 'app_name'
    FIELD_COMPANY_ID = 'appannie_company_id'
    FIELD_PUBLISHER_ID = 'appannie_publisher_id'
    FIELD_OWNER_NAME = 'owner_name'
    FIELD_CRAWL_DATE = 'appannie_crawl_date'
    FIELD_HAS_IAP = 'has_iap'
    FIELD_RELEASE_DATE_STR = 'release_date_str'
    FIELD_LAST_UPDATE_DATE_STR = 'last_update_date_str'
    FIELD_UPDATE_TIME = 'update_time'
    FIELD_QUERY_DATE = 'query_date'
    FIELD_FEED_TYPE = 'feed_type'
    FIELD_ICON_ID = 'icon_id'
    FIELD_COUNTRY = 'country'


class AndroidTopColumn:
    RANKING = '#'
    APP_INFO = 'App'
    RANKING_CHANGE_FREE = 'Free Rank'
    RANKING_CHANGE_NEW_FREE = 'New Free Rank'
    RANKING_CHANGE_GROSSING = 'Grossing Rank'
    RANKING_CHANGE_PAID = 'Paid Rank'
    RANKING_CHANGE_NEW_PAID = 'New Paid Rank'
    SUB_CATEGORY = 'Category'
    RELEASE_DATE = 'Release Date'
    LAST_UPDATE_DATE = 'Last Update'


class AndroidTopDBFiled:
    FIELD_RANKING = 'ranking'
    FIELD_SUB_CATEGORY = 'sub_category'
    FIELD_RANKING_CHANGE = 'ranking_change'
    FIELD_APP_ID = 'appannie_app_id'
    FIELD_APP_NAME = 'app_name'
    FIELD_COMPANY_ID = 'appannie_company_id'
    FIELD_PUBLISHER_ID = 'appannie_publisher_id'
    FIELD_OWNER_NAME = 'owner_name'
    FIELD_CRAWL_DATE = 'appannie_crawl_date'
    FIELD_HAS_IAP = 'has_iap'
    FIELD_RELEASE_DATE_STR = 'release_date_str'
    FIELD_LAST_UPDATE_DATE_STR = 'last_update_date_str'
    FIELD_UPDATE_TIME = 'update_time'
    FIELD_QUERY_DATE = 'query_date'
    FIELD_FEED_TYPE = 'feed_type'
    FIELD_ICON_ID = 'icon_id'
    FIELD_COUNTRY = 'country'


if __name__ == '__main__':
    print(IOSTopDBFiled.FIELD_RANKING)
