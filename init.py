# -*- coding:utf-8 -*-
import os
import settings as _s

if not os.path.exists(_s.default_data_store_dir):
    os.makedirs(_s.default_data_store_dir)
if not os.path.exists(_s.default_screenshot_dir):
    os.makedirs(_s.default_screenshot_dir)
if not os.path.exists(_s.default_log_dir):
    os.makedirs(_s.default_log_dir)
if not os.path.exists(_s.default_cookies_dir):
    os.makedirs(_s.default_cookies_dir)
