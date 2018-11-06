# -*- coding:utf-8 -*-


class TopAppDBField:
    FIELD_APP_ID = 'appannie_app_id'
    FIELD_DEVELOPER_ID = 'developer_id'
    FIELD_STORE_URL = 'app_store_url'
    FIELD_DEVELOPER_NAME = 'developer_name'
    FIELD_APP_NAME = 'app_name'
    FIELD_OS = 'os'
    FIELD_RELEASE_DATE = 'release_date'
    FIELD_LAST_UPDATE_DATE = 'last_update_date'
    FIELD_COMPANY_ID = 'appannie_company_id'
    FIELD_PUBLISHER_ID = 'appannie_publisher_id'
    FIELD_OWNER_NAME = 'owner_name'
    FIELD_CATEGORY = 'category'
    FIELD_UPDATE_TIME = 'update_time'
    FIELD_DETAIL_ID = 'appannie_detail_id'
    FIELD_UNIFIED_APP_ID = 'unified_app_id'

    @staticmethod
    def get_all_fields():
        ret = []
        obj_me = TopAppDBField()
        for _x in TopAppDBField.__dict__:
            if _x.startswith('FIELD'):
                ret.append(TopAppDBField.__getattribute__(obj_me, _x))
        return ret


if __name__ == '__main__':
    print(TopAppDBField().get_all_fields())
