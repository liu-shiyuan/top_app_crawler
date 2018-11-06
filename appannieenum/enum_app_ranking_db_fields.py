# -*- coding:utf-8 -*-


class AppRankingDBField:
    # FIELD_ID = 'id'
    FIELD_CATEGORY = 'category'
    FIELD_RANKING = 'ranking'
    FIELD_RANKING_CHANGE = 'ranking_change'
    FIELD_APP_ID = 'appannie_app_id'
    FIELD_APP_NAME = 'app_name'
    FIELD_APPANNIE_CRAWL_DATE = 'appannie_crawl_date'
    FIELD_HAS_IAP = 'has_iap'
    FIELD_UPDATE_TIME = 'update_time'
    FIELD_QUERY_DATE = 'query_date'
    FIELD_FEED_TYPE = 'feed_type'
    FIELD_ICON_ID = 'icon_id'
    FIELD_COUNTRY = 'country'
    FIELD_OS = 'os'
    FIELD_QUERY_CATEGORY = 'query_category'

    @staticmethod
    def get_all_fields():
        ret = []
        obj_me = AppRankingDBField()
        for _x in AppRankingDBField.__dict__:
            if _x.startswith('FIELD'):
                ret.append(AppRankingDBField.__getattribute__(obj_me, _x))
        return ret


if __name__ == '__main__':
    # for _x in AppRankingDBField.__dict__:
    #     print(_x)
    print(AppRankingDBField().get_all_fields())
