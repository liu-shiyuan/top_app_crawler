# coding=utf8
from commonutils import get_cst_to_machine_hour_and_minute
from datetime import datetime
from loggers import get_misfire_logger
from appannieenum import OSType, ios_game_category_names, android_game_category_names
from crawltask.ios_crawl_task import run_ios_top_task
from crawltask.android_crawl_task import run_android_top_task
from crawltask.refire_queue import get_queue, add_re_fire_job


_re_fire_time_range = ('00:00', '04:30')
_start_time = get_cst_to_machine_hour_and_minute(_re_fire_time_range.__getitem__(0))
_stop_time = get_cst_to_machine_hour_and_minute(_re_fire_time_range.__getitem__(1))


def re_fire():
    # while True:
    #     now_time = datetime.now().strftime('%H:%M')
    #     if _start_time <= now_time <= _stop_time:
    #         _do_re_fire()
    _do_re_fire()


def _do_re_fire():
    _misfire_jobs = get_queue()
    while _misfire_jobs and not _misfire_jobs.empty():
        re_fire_job = _misfire_jobs.get()
        if re_fire_job:
            try:
                category_code = _get_category_code(re_fire_job.os, re_fire_job.category)
                if re_fire_job.os == OSType.Android:
                    run_android_top_task(country=re_fire_job.country, query_date=re_fire_job.query_date,
                                         sub_category_code=category_code, feed=re_fire_job.feed_type)
                elif re_fire_job.os == OSType.IOS:
                    run_ios_top_task(country=re_fire_job.country, query_date=re_fire_job.query_date,
                                     sub_category_code=category_code, feed=re_fire_job.feed_type)
                get_misfire_logger().info('done for: ' + str(re_fire_job))
            except Exception as e:
                get_misfire_logger().info('ERROR for: ' + str(re_fire_job))
                get_misfire_logger().info(e.__str__())
                add_re_fire_job(re_fire_job)


def _get_category_code(os, category_name):
    category_names = ios_game_category_names if os == OSType.IOS else android_game_category_names
    for _category in category_names:
        if _category['display'] == category_name:
            return _category['code']
    return None


if __name__ == '__main__':
    a = _get_category_code(1, 'Role Playing')
    print(a)
