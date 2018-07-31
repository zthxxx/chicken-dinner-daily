import logging

from aip import AipOcr

from config import config
from lib.utils.ocr import save_captcha
from lib.utils.request import base64_dataurl

APP_ID = config['baidu_aip']['app_id']
API_KEY = config['baidu_aip']['api_key']
SECRET_KEY = config['baidu_aip']['secret_key']

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def aip_ocr(data_url):
    logging.info('request aip ocr api.')
    img_base64 = base64_dataurl(data_url)
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
