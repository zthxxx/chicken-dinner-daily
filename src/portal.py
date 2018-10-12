from base64 import b64encode
import json
import logging
import re

from config import config
from lib.utils.request import request, request_content

PORTAL_BASE = {
    'os_name': 'Mac OS',
    'browser_name': 'chrome 69.0',
    'force_change': 0,
    'request_url': 'https://google.com/'
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
    logging.info(f'portal post status: <{portal_res.status_code}>')
    logging.debug(portal_res.request.headers)
    logging.info(portal_res.json())


def run():
    csrf_token = get_csrf_token()
    pass_portal(csrf_token)


run()
