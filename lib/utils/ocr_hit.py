import logging
import os
import time

CAPTCHA_DIR = 'captcha-test'
captchas = os.listdir(CAPTCHA_DIR)
captchas = list(filter(lambda file: 'captcha_' not in file, captchas))


def get_img_content(img):
    with open(img, 'rb') as fp:
        return fp.read()


def ocr_hit(ocr2str):
    matched = 0
    for captcha in captchas:
        image = get_img_content(f'{CAPTCHA_DIR}/{captcha}')
        captcha = os.path.splitext(captcha)[0]
        results = ocr2str(image)
        match_tip = ''
        if captcha in results:
            matched += 1
            match_tip = 'has matched'
        logging.info((captcha, results, match_tip))
        time.sleep(0.5)
    hit_rate = matched / len(captchas) * 100
    logging.info(f'total is {len(captchas)}, matched {matched}, hit rate {hit_rate}%')
