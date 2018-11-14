# coding=utf8
from queue import Queue
from commonutils import MisfireJob

_misfire_jobs = Queue()


def get_queue():
    return _misfire_jobs


def add_re_fire_job(re_fire_job):
    _misfire_jobs.put(re_fire_job)
