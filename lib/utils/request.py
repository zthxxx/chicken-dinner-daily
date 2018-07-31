from lxml import html
import requests

DATAURL_HEADER = 'data:image/jpeg;base64,'


def request_content(url, method='get', **kwargs):
    response = request.request(method, url, **kwargs)
    response.encoding = response.apparent_encoding
    return response.text, response.status_code


def request_dom(url, *args, **kwargs):
    response, _ = request_content(url, *args, **kwargs)
    return html.fromstring(response)


def get_attrib(dom, select, attr):
    return dom.cssselect(select)[0].attrib.get(attr)


def reset_request():
    req = requests.Session()
    req.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    })
    return req


def base64_dataurl(data_url):
    return data_url.replace(DATAURL_HEADER, '')


request = reset_request()
