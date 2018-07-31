import json
import logging
import time

from lxml import html
from retrying import retry

from config import config
from lib.utils.request import get_attrib, request_content, request_dom, reset_request
from src.juhe_vercode import juhe_ocr

login_url = config['login']['url']
login_page = request_dom(login_url)

status = 200
ocr_method = juhe_ocr

while status != 302:
    token = get_attrib(login_page, '#token', 'value')
    captcha_base64 = get_attrib(login_page, '#captcha', 'src')

    ocr_str = ocr_method(captcha_base64)
    while not ocr_str:
        time.sleep(1.2)
        captcha_base64, _ = request_content(config['login']['captcha'])
        ocr_str = ocr_method(captcha_base64)

    login_args = {
        'logintype': 0,
        'user': config['login']['username'],
        'password': config['login']['password'],
        '_token': token,
        'phrase': ocr_str
    }

    res, status = request_content(login_url, method='post', data=login_args)
    if status == 200:
        logging.warning('captcha is error, retry it')
        time.sleep(2.5)
        login_page = html.fromstring(res)
    if status == 500:
        logging.info('session or server is error, retry it')
        time.sleep(5)
        reset_request()
        login_page = request_dom(login_url)
    if status == 302:
        logging.info(('login ok', res, status))

base_page = request_dom(config['punch']['base'])
token = get_attrib(base_page, '#token', 'value')


punch_api = config['punch']['api']
punch_args = json.dumps({'_token': token})


@retry(wait_random_min=3000, wait_random_max=5000,
       retry_on_result=lambda code: code != 200)
def retry_punch(api, args):
    res, status = request_content(api, method='post', data=args)
    logging.info(('punch submit', res, status))
    return status


retry_punch(punch_api, punch_args)

