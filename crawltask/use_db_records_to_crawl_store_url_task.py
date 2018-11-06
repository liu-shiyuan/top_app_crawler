# -*- coding:utf-8 -*-
from thecrawler import IterateTopAppInsert
import os
from loggers import get_logger
from db import tmp_func_query_app_id_list


# todo country specific
def _do_task():
    """ program bug may cause some app store url not crawled, this task may fix that issue."""
    records = tmp_func_query_app_id_list()
    exclude_set = None
    exclude_set_file = 'data/already_removed.txt'
    if records:
        get_logger().info('records count %s' % str(len(records)))
        if os.path.exists(exclude_set_file):
            with open(exclude_set_file, 'r') as f:
                exclude_set = [x.strip() for x in f.readlines()]
            if exclude_set:
                records = [x for x in records if x['appannie_app_id'] not in exclude_set]
            get_logger().info('records count %s' % str(len(records)))
            IterateTopAppInsert(records).do_insert()
    get_logger().info('base on db records crawl store url: DONE')


if __name__ == '__main__':
    _do_task()
