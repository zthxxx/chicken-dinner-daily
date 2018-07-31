import logging
import time

from lxml import html
from retrying import retry

from config import config
from lib.utils.request import get_attrib, request_content, request_dom, reset_request
from lib.captcha.airp import aip_ocr

image2str = aip_ocr


def init_connection():
    login_url = config['login']['url']
    login_page = request_dom(login_url)
    return login_page


def get_captcha_str(login_page):
    captcha_dataurl = get_attrib(login_page, '#captcha', 'src')
    captcha = image2str(captcha_dataurl)
    while not captcha:
        time.sleep(1.2)
        captcha_dataurl, _ = request_content(config['login']['captcha'])
        captcha = image2str(captcha_dataurl)
    return captcha


def login(token, captcha):
    """
    :param captcha: str of captcha
    :return: is_logined, logined_page
    """
    login_args = {
        'logintype': 0,
        'user': config['login']['username'],
        'password': config['login']['password'],
        '_token': token,
        'phrase': captcha
    }
    login_url = config['login']['url']
    res, status = request_content(login_url, method='post', data=login_args)
    if status != 200:
        logging.info('session or server is error, retry it')
        reset_request()
        return False, init_connection()
    login_flag = '验证码错误' not in res
    if login_flag:
        logging.info(('login ok', res, status))
    else:
        logging.warning('captcha is error, retry it')
    return login_flag, html.fromstring(res)


def retry_login(login_page):
    token = get_attrib(login_page, '#token', 'value')
    captcha = get_captcha_str(login_page)
    login_flag, next_page = login(token, captcha)
    if login_flag:
        return next_page
    else:
        return retry_login(next_page)


@retry(wait_random_min=3000, wait_random_max=5000,
       retry_on_result=lambda code: code != 200)
def retry_punch(api, args):
    res, status = request_content(api, method='post', data=args)
    logging.info(('punch submit', res, status))
    return status


def punch(punch_page):
    token = get_attrib(punch_page, '#token', 'value')
    punch_api = config['punch']['api']
    punch_args = {'_token': token}
    retry_punch(punch_api, punch_args)


def run():
    login_page = init_connection()
    punch_page = retry_login(login_page)
    punch(punch_page)


run()
