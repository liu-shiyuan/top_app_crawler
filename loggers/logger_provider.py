# -*- coding:utf-8 -*-
import logging.config
import settings as _s


_project_work_dir = _s.current_dir
_log_conf_file_path = _project_work_dir + 'logger.conf'
logging.config.fileConfig(_log_conf_file_path)
__logger__ = logging.getLogger('fileLogger')
_misfire_logger = logging.getLogger('misfireLogger')


def get_logger():
    return __logger__


def get_misfire_logger():
    return _misfire_logger


if __name__ == '__main__':
    get_logger().info('fffff')
