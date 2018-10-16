import os
import re
import logging

from config import config


def get_ssid():
    airport_cmd = """airport -I | awk -F ': ' '/ SSID/ {printf("%s", $2)}'"""
    popen = os.popen(airport_cmd)
    ssid = popen.read()
    return ssid


def ssid_matched():
    ssid = get_ssid()
    ssid_pattern = re.compile(config['ssid_pattern'])
    return ssid_pattern.match(ssid)


def assert_ssid_matched():
    if not ssid_matched():
        logging.info(f'WiFi SSID not match ({config["ssid_pattern"]})')
        exit(0)
