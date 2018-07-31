import logging

from config import config
from lib.utils.ocr import save_captcha
from lib.utils.request import base64_dataurl, reset_request

request = reset_request()


def juhe_ocr(data_url):
    logging.info('request juhe vercode api.')
    img_base64 = base64_dataurl(data_url)
    save_captcha(img_base64)
    data = {
        'key': config['juhe']['app_key'],
        'codeType': config['juhe']['type_code'],
        'base64Str': img_base64,
        'dtype': 'json'
    }
    api_url = config['juhe']['api']

    response = request.request('post', api_url, data=data, timeout=100)
    if response.status_code != 200:
        logging.error(['error juhe api', response.text])
        return None
    result = response.json()
    if result['error_code'] is 0:
        return result['result']
    logging.warning(['error juhe api', result['reason']])
    return None
