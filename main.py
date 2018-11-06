# -*- coding:utf-8 -*-
import schedule
from crawltask.ios_crawl_task import run_ios_top_task
from crawltask.android_crawl_task import run_android_top_task
from appannieenum import AppannieCountry
import time
from loggers import get_logger
from commonutils import get_cst_yesterday, get_cst_to_machine_hour_and_minute
from crawltask.fix_broken_app_icon_task import fix_daily_app_icon_task
from multiprocessing import Process


def job_queue_1():
    query_date = get_cst_yesterday()
    get_logger().info('do job_queue_1: %s' % query_date)
    run_ios_top_task(country=AppannieCountry.UNITED_STATE, query_date=query_date)
    run_android_top_task(country=AppannieCountry.UNITED_STATE, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.JAPAN, query_date=query_date)
    run_android_top_task(country=AppannieCountry.JAPAN, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.INDONESIA, query_date=query_date)
    run_android_top_task(country=AppannieCountry.INDONESIA, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.SINGAPORE, query_date=query_date)
    run_android_top_task(country=AppannieCountry.SINGAPORE, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.MALAYSIA, query_date=query_date)
    run_android_top_task(country=AppannieCountry.MALAYSIA, query_date=query_date)
    get_logger().info('fix_daily_app_icon_task: %s' % query_date)
    fix_daily_app_icon_task(query_date)


def job_queue_2():
    query_date = get_cst_yesterday()
    get_logger().info('do job_queue_2: %s' % query_date)
    run_ios_top_task(country=AppannieCountry.REPUBLIC_OF_KOREA, query_date=query_date)
    run_android_top_task(country=AppannieCountry.REPUBLIC_OF_KOREA, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.FRANCE, query_date=query_date)
    run_android_top_task(country=AppannieCountry.FRANCE, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.THAILAND, query_date=query_date)
    run_android_top_task(country=AppannieCountry.THAILAND, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.HONG_KONG, query_date=query_date)
    run_android_top_task(country=AppannieCountry.HONG_KONG, query_date=query_date)
    run_ios_top_task(country=AppannieCountry.TAIWAN, query_date=query_date)
    run_android_top_task(country=AppannieCountry.TAIWAN, query_date=query_date)
    get_logger().info('fix_daily_app_icon_task: %s' % query_date)
    fix_daily_app_icon_task(query_date)


def queue_1_process():
    p = Process(target=job_queue_1)
    p.start()


def queue_2_process():
    p = Process(target=job_queue_2)
    p.start()


if __name__ == '__main__':
    cst_start_ios_job_time_str = '05:00'
    cst_start_android_job_time_str = '05:03'

    ios_job_time = get_cst_to_machine_hour_and_minute(cst_start_ios_job_time_str)
    adr_job_time = get_cst_to_machine_hour_and_minute(cst_start_android_job_time_str)
    get_logger().info('schedule ios job at: %s' % ios_job_time)
    get_logger().info('schedule android job at: %s' % adr_job_time)
    get_logger().info('this round crawl job query date: %s' % get_cst_yesterday())

    schedule.every().day.at(ios_job_time).do(queue_1_process)
    schedule.every().day.at(adr_job_time).do(queue_2_process)

    while True:
        schedule.run_pending()
        time.sleep(1)
