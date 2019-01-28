import requests
import datetime
import json


def http_post(host, api, headers, data, port=80, timeout=10):
    """
    :param api: /login
    :param headers: headers
    :param data: body
    """
    if api.startswith('/'):
        api = api[1:]
    url = "%s:%s/%s" % (host, port, api)
    response = requests.post(url=url, data=json.dumps(data), headers=headers, timeout=timeout)
    return response.json()


def http_get(host, data={}, api='', headers={}):
    """
    :param api: /login
    :param headers: headers
    :param data: payload
    """
    if api.startswith('/'):
        api = api[1:]
    url = "%s/%s" % (host, api)
    print("wechat http GET: %s, %s" % (url, str(data)))
    res = requests.get(url, headers=headers, params=data)
    return res


def dt2ts(dt=None, place=10):
    if dt is None:
        dt = datetime.datetime.now()
    assert isinstance(dt, datetime.datetime)
    assert place in (10, 13)
    if place == 10:
        return int(dt.timestamp())
    if place == 13:
        return int(dt.timestamp()) * 1000

chunk_size=1024
def save_stream(fname, stream):
    with open(fname, 'wb') as fd:
        for chunk in stream.iter_content(chunk_size):
            fd.write(chunk)


def run():

    host='http://dynamic.rbc.cn/soms4/web/jwzt/player/'
    api='getRecordList.jsp'
    headers={
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", 
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.rbc.cn/audio/2017gbhf.shtml",
        "Cookie": "JSESSIONID=9B27A621447902959986DB34FBEB95D5.tomcat23301; vjuids=-5d2784ded.1683c4a666d.0.96f3e80133cb8; vjlast=1547199735.1547199735.30; Hm_lvt_3c34e141c7ebb87024721850c93c123b=1547199735; Hm_lpvt_3c34e141c7ebb87024721850c93c123b=1547199742",
    }
    data = dict(
        programName='感受北京 Touch Beijing（重播）',
        planId=5002513,
        start=0,
        limit=20,
        jsoncallback='jQuery21105429139183596063_1547264955666',
        _=dt2ts(place=13)
    )

    res = http_get(host, data=data, api=api, headers=headers)
    # print(res)
    print(dir(res))
    # print(res.text)
    # print(res.json())
    text = res.text.strip()
    json_s = text[len("jQuery21105429139183596063_1547264955666("):-1]
    res_dict = json.loads(json_s)
    for item in res_dict['programs']:
        fname = '/Users/mz/Downloads/感受北京.' + item['file_name'][-8:] + '.mp4'
        stream_url = item['file_streaming']
        stream = requests.get(stream_url, stream=True)
        save_stream(fname, stream)
        break

if __name__ == '__main__':
    run()


