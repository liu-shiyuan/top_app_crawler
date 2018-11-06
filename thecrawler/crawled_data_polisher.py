# -*- coding:utf-8 -*-
from db import TopAppDBHandler, is_valid_record
from appannieenum import TopAppDBField, AppRankingDBField, OSType

_invalid_str = '******'


class CrawledDataPolisher:
    def __init__(self):
        pass

    @staticmethod
    def polish(data, os):
        if not data:
            return
        top_app_handler = TopAppDBHandler()
        try:
            top_app_handler.open_conn()
            for _record in data:
                if not _record[AppRankingDBField.FIELD_CATEGORY]:
                    continue
                db_record = None
                if OSType.IOS == os:
                    db_record = top_app_handler.query_record_by_app_id(_record[TopAppDBField.FIELD_APP_ID])
                elif OSType.Android == os:
                    db_record = top_app_handler.query_record_by_unified_app_id(_record[TopAppDBField.FIELD_UNIFIED_APP_ID])
                if db_record and not is_valid_record(_record):
                    if _record[AppRankingDBField.FIELD_APP_NAME] is None or \
                            _invalid_str == _record[AppRankingDBField.FIELD_APP_NAME]:
                        _record[AppRankingDBField.FIELD_APP_NAME] = db_record[AppRankingDBField.FIELD_APP_NAME]
                    if _record[TopAppDBField.FIELD_DETAIL_ID] is None or \
                            _invalid_str == _record[TopAppDBField.FIELD_DETAIL_ID]:
                        _record[TopAppDBField.FIELD_DETAIL_ID] = db_record[TopAppDBField.FIELD_DETAIL_ID]
                    if _record[TopAppDBField.FIELD_PUBLISHER_ID] is None or \
                            _invalid_str == _record[TopAppDBField.FIELD_PUBLISHER_ID]:
                        _record[TopAppDBField.FIELD_PUBLISHER_ID] = db_record[TopAppDBField.FIELD_PUBLISHER_ID]
                    if _record[TopAppDBField.FIELD_COMPANY_ID] is None or \
                            _invalid_str == _record[TopAppDBField.FIELD_COMPANY_ID]:
                        _record[TopAppDBField.FIELD_COMPANY_ID] = db_record[TopAppDBField.FIELD_COMPANY_ID]
                    if _record[TopAppDBField.FIELD_OWNER_NAME] is None or \
                            _invalid_str == _record[TopAppDBField.FIELD_OWNER_NAME]:
                        _record[TopAppDBField.FIELD_OWNER_NAME] = db_record[TopAppDBField.FIELD_OWNER_NAME]
        except Exception as e:
            raise e
        finally:
            if top_app_handler:
                top_app_handler.close_conn()
