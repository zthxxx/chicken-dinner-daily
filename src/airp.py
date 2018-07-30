import os
import time
import logging
import base64
from datetime import datetime

from aip import AipOcr

from config import config
from lib.conffor import ensure_dir_exist

logging.basicConfig(level=logging.INFO)

APP_ID = config['ocr']['app_id']
API_KEY = config['ocr']['api_key']
SECRET_KEY = config['ocr']['secret_key']

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

CAPTCHA_DIR = 'captcha-test'
dataurl_header = 'data:image/jpeg;base64,'
captchas = os.listdir(CAPTCHA_DIR)
captchas = list(filter(lambda file: 'captcha_' not in file, captchas))


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
    img_base64 = data_url.replace(dataurl_header, '')
    save_captcha(img_base64)
    res = client.webImage(bytes(), options={
        'image': img_base64
    })
    if 'words_result_num' not in res or res['words_result_num'] is 0:
        logging.info((f'aip have not result', res))
        return []
    results = [result['words'] for result in res['words_result']]
    results = list(filter(lambda word: len(word) is 5, results))
    return results[0] if results else None


def aip_test():
    matched = 0
    for captcha in captchas:
        image = get_img_content(f'{CAPTCHA_DIR}/{captcha}')
        res = client.webImage(image)
        captcha = os.path.splitext(captcha)[0]
        if 'words_result_num' not in res or res['words_result_num'] is 0:
            logging.info(f'{captcha}  aip have not result')
            continue
        results = [result['words'] for result in res['words_result']]
        match_tip = ''
        if captcha in results:
            matched += 1
            match_tip = 'has matched'
        logging.info((captcha, results, match_tip))
        time.sleep(0.5)
    hit_rate = matched / len(captchas) * 100
    logging.info(f'total is {len(captchas)}, matched {matched}, hit rate {hit_rate}%')


