import logging

from bs4 import BeautifulSoup
import requests

HTML_PARSER = 'html.parser'
DATAURL_HEADER = 'data:image/jpeg;base64,'


def html(markup):
    return BeautifulSoup(markup, HTML_PARSER)


def request_content(url, method='get', **kwargs):
    response = request.request(method, url, **kwargs)
    logging.debug(f'''
    request url {url}
    response  {response.text[:20]}
    ''')
    return response.text, response.status_code


def request_dom(url, *args, **kwargs):
    response, _ = request_content(url, *args, **kwargs)
    return html(response)


def get_attrib(dom, select, attr):
    return dom.select(select)[0].attrs.get(attr)


def reset_request():
    req = requests.Session()
    req.headers.update({
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    })
    return req


def base64_dataurl(data_url):
    return data_url.replace(DATAURL_HEADER, '')


request = reset_request()
