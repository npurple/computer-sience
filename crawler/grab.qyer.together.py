# coding=utf8
'''
    穷游网结伴数据
'''

import json
import requests
from pprint import pprint

host = 'https://bbs.qyer.com/'
def http_post(host, api, headers, data, port=None, timeout=10):
    """
    :param api: /login
    :param headers: headers
    :param data: body
    """
    if api.startswith('/'):
        api = api[1:]
    if port:
        url = "%s:%s/%s" % (host, port, api)
    else:
        url = "%s/%s" % (host, api)
    print(url)
    response = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=timeout)
    return response.json()


def page_detail(api):
    pass


def page_list():
    api = 'thread.php?action=getTogether'
    payload = dict(
        page=1,
        limit=20
    )
    response = http_post(host, api, {}, payload)
    pprint(response)
