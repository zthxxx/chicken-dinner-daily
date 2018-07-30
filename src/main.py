import time
import json
import logging

from lxml import html

from config import config
from src.airp import aip_ocr
from lib.utils.request import reset_request, request_content, request_dom, get_attrib

login_url = config['login']['url']
login_page = request_dom(login_url)

status = 200

while status is not 302:
    token = get_attrib(login_page, '#token', 'value')
    captcha_base64 = get_attrib(login_page, '#captcha', 'src')

    ocr_str = aip_ocr(captcha_base64)
    while not ocr_str:
        time.sleep(1.2)
        captcha_base64, _ = request_content(config['login']['captcha'])
        ocr_str = aip_ocr(captcha_base64)

    login_args = {
        'logintype': 0,
        'user': config['login']['username'],
        'password': config['login']['password'],
        '_token': token,
        'phrase': ocr_str
    }

    res, status = request_content(login_url, method='post', data=login_args)
    if status is 200:
        logging.info('captcha is error, retry it')
        time.sleep(2.5)
        login_page = html.fromstring(res)
    if status is 500:
        logging.info('session or server is error, retry it')
        time.sleep(5)
        reset_request()
        login_page = request_dom(login_url)
    if status is 302:
        print(res)

base_page = request_dom(config['punch']['base'])
token = get_attrib(base_page, '#token', 'value')

punch_args = json.dumps({'_token': token})
punch_api = config['punch']['api']
res, status = request_content(login_url, method='post', data=punch_args)
print(res, status)



