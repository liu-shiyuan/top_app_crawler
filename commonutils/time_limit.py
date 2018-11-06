# -*- coding:utf-8 -*-
import signal
from contextlib import contextmanager
import platform


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds, msg=None):
    if 'linux' == platform.system().lower():
        def signal_handler(signum, frame):
            raise TimeoutException(msg or "Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    else:
        yield


if __name__ == '__main__':
        try:
            with time_limit(15):
                1 / 0
        except TimeoutException as e:
            print(e.reason)