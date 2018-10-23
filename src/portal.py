from base64 import b64encode
import json
import logging
import re

from retrying import retry
from requests.exceptions import RequestException

from config import config
from lib.utils.airport import assert_ssid_matched
from lib.utils.request import request, request_content
from lib.utils.notify import notify

PORTAL_BASE = {
    'os_name': 'Mac OS',
    'browser_name': 'chrome 69.0',
    'force_change': 0
}


def get_csrf_token():
    login_page, status = request_content(config['portal']['route'])
    logging.info(f'portal login page status: <{status}>')
    token_pattern = re.compile('\{"csrf_token": "(?P<csrf_token>.*)"\}')
    csrf_token = token_pattern.search(login_page).group('csrf_token')
    return csrf_token


def pass_portal(csrf_token):
    request.headers.update({'X-CSRFToken': csrf_token})

    password = b64encode(config['login']['password'].encode()).decode()

    portal_args = {
        'user_name': config['login']['username'],
        'pwd': password,
        **PORTAL_BASE
    }

    portal_res = request.post(config['portal']['api'], data=portal_args)
    status_code = portal_res.status_code
    logging.info(f'portal post status: <{status_code}>')
    logging.debug(portal_res.request.headers)
    result = portal_res.json()
    logging.info(result)
    portal_status = result.get('reason') == 'success'
    notify('Portal Post', '🎉 Success' if portal_status else '💥 Failed')


@retry(wait_random_min=3000, wait_random_max=5000,
       stop_max_attempt_number=3)
def portal_post():
    csrf_token = get_csrf_token()
    pass_portal(csrf_token)


def run():
    logging.info('WLAN portal start.')
    assert_ssid_matched()
    try:
        portal_post()
    except RequestException as e:
        notify('💥 Portal Failed', f'Request Error: {e}')

run()
