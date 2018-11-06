# -*- coding:utf-8 -*-
from selenium.common.exceptions import NoSuchElementException
import settings as _s
import time
from loggers import get_logger
from manageraccounts import load_accounts


def asking_me_areyouhuman(_driver):
    try:
        _capcha_elem = _driver.find_element_by_id(_s.appannie_captcha_form_id)
        if _capcha_elem:
            return True
    except NoSuchElementException as e:
        pass
    return False


def is_on_error_page(_driver):
    try:
        _body = _driver.find_element_by_tag_name('body')
        if _body:
            _clzz = _body.get_attribute('class')
            if _clzz and _s.appannie_block_account_body_class in _clzz:
                return True
    except NoSuchElementException as e:
        pass
    return False


def oops_account_has_been_blocked(_driver):
    try:
        ele_containers = _driver.find_elements_by_class_name('content-container')
        if ele_containers:
            ele_container = ele_containers[0]
            error_msg = ele_container.text
            if 'you are not authorised to view this webpage' in error_msg:
                return True
    except NoSuchElementException as e:
        pass
    return False


def oops_request_problem_occurred(_driver):
    try:
        ele_containers = _driver.find_elements_by_class_name('content-container')
        if ele_containers:
            ele_container = ele_containers[0]
            error_msg = ele_container.text
            if 'There was a problem processing your request' in error_msg:
                return True
    except NoSuchElementException as e:
        pass
    return False


def wait_account_to_continue(country, blocked_fun_name=None):
    with load_accounts(country) as accounts:
        while not accounts:
            if blocked_fun_name:
                get_logger().info('%s wait account to continue..' % blocked_fun_name)
            else:
                get_logger().info('wait account to continue..')
            time.sleep(60)


def app_has_been_removed(_driver):
    try:
        _status_spans = _driver.find_elements_by_class_name('status')
        if _status_spans:
            for _status_span in _status_spans:
                if hasattr(_status_span, 'text'):
                    _text = _status_span.text
                    if 'This app has been removed from the store' in _text \
                            or 'This app bundle has been removed from the store' in _text:
                        return True
        return False
    except Exception as e:
        return False
