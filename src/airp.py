import logging
import base64
from datetime import datetime
import logging

from aip import AipOcr

from config import config
from lib.conffor import ensure_dir_exist
from lib.utils.ocr_hit import CAPTCHA_DIR
from lib.utils.request import base64_dataurl

APP_ID = config['baidu_aip']['app_id']
API_KEY = config['baidu_aip']['api_key']
SECRET_KEY = config['baidu_aip']['secret_key']

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_img_content(img):
    with open(img, 'rb') as fp:
        return fp.read()


def save_captcha(img_base64):
    image = base64.b64decode(img_base64)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    image_file = f'{CAPTCHA_DIR}/captcha_{timestamp}.jpg'
    ensure_dir_exist(image_file)
    with open(image_file, 'wb+') as fp:
        fp.write(image)


def aip_ocr(data_url):
    logging.info('request aip ocr api.')
    img_base64 = base64_dataurl(data_url)
    save_captcha(img_base64)
    res = client.basicAccurate(bytes(), options={
        'image': img_base64
    })
    if 'words_result_num' not in res or res['words_result_num'] is 0:
        logging.info((f'aip have not result', res))
        return []
    results = [result['words'] for result in res['words_result']]
    results = list(filter(lambda word: len(word) is 5, results))
    return results[0] if results else None


def aip_test(image):
    res = client.webImage(image)
    if 'words_result_num' not in res or res['words_result_num'] is 0:
        logging.info(f'aip have not result')
        return ['aip have NOT any result']
    results = [result['words'] for result in res['words_result']]
    return results
