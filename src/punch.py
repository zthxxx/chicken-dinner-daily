import logging
import time
import json

from retrying import retry

from config import config
from lib.utils.airport import assert_ssid_matched
from lib.utils.request import get_attrib, html, request_content, request_dom, reset_request
from lib.utils.notify import notify

HTML_PARSER = 'html.parser'


def init_connection():
    login_url = config['punch']['route']
    login_page = request_dom(login_url)
    return login_page


def login(token):
    """
    :return: is_logined, logined_page
    """
    login_args = {
        'logintype': 0,
        'username': config['login']['username'],
        'password': config['login']['password'],
        'sso_failnum': '',
        '_token': token
    }
    login_url = config['punch']['route']
    res, status = request_content(login_url, method='post', data=login_args)
    if status != 200:
        logging.info('session or server is error, retry it')
        reset_request()
        return False, init_connection()
    logging.info(('login ok, status:', status))
    logging.debug(('login-ok page raw:', res))
    return True, html(res)


def retry_login(login_page):
    token = get_attrib(login_page, 'input[name="_token"]', 'value')
    login_flag, next_page = login(token)
    if login_flag:
        return next_page
    else:
        time.sleep(2)
        return retry_login(next_page)


def find_subsystem(sso_page, subsystem):
    subsystem_anchors = sso_page.select('div.ibox-content .row ul li a')
    for anchor in subsystem_anchors:
        if subsystem in anchor.text:
            href = anchor.attrs.get('href')
            return request_dom(href)


@retry(wait_random_min=3000, wait_random_max=5000,
       stop_max_attempt_number=3,
       retry_on_result=lambda code: code // 100 != 2)
def retry_punch(api, args):
    res, status = request_content(api, method='post', data=args)
    result = json.loads(res)
    message = result.get('message', '')
    logging.info(('punch submit', result, status))
    notify('Punch Dinner', message)
    if '成功' in message or '未到打卡时间' in message:
        return status
    return 500


def punch(punch_page):
    token = get_attrib(punch_page, '#token', 'value')
    punch_args = {'_token': token}
    punch_api = config['punch']['api']
    retry_punch(punch_api, punch_args)


def run():
    logging.info('winner winner, chicken dinner')
    assert_ssid_matched()
    login_page = init_connection()
    sso_page = retry_login(login_page)
    punch_page = find_subsystem(sso_page, '人事系统')
    punch(punch_page)


run()
