import base64
from datetime import datetime
import logging
import os
import time

from lib.conffor import ensure_dir_exist

CAPTCHA_DIR = 'captcha-test'
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
    return image_file


def ocr_hit(ocr2str):
    matched = 0
    for captcha in captchas:
        image = get_img_content(f'{CAPTCHA_DIR}/{captcha}')
        captcha = os.path.splitext(captcha)[0]
        result = ocr2str(image)
        match_tip = ''
        if result == captcha:
            matched += 1
            match_tip = 'has matched'
        logging.info((captcha, result, match_tip))
        time.sleep(0.5)
    hit_rate = matched / len(captchas) * 100
    logging.info(f'total is {len(captchas)}, matched {matched}, hit rate {hit_rate}%')
