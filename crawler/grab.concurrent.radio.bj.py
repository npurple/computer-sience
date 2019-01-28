import os
import time
import json
import requests
import datetime
import asyncio
import aiohttp
from concurrent import futures



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
async def download_stream(fname, url):
    print(fname, url)
    if os.path.exists(fname):
        print('file already exist')
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # print(dir(resp))
            # print(dir(resp.read()))
            with open(fname, 'wb') as fd:
                stream = await resp.read()
                fd.write(stream)
                # for chunk in resp.read(chunk_size):
                #     await fd.write(chunk)

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
    start = 0
    size = 20
    while 1:
        data = dict(
            programName='感受北京 Touch Beijing（重播）',
            planId=5002513,
            start=start,
            limit=size,
            jsoncallback='jQuery21105429139183596063_1547264955666',
            _=dt2ts(place=13)
        )

        res = http_get(host, data=data, api=api, headers=headers)
        # print(res)
        # print(dir(res))
        # print(res.text)
        # print(res.json())
        text = res.text.strip()
        json_s = text[len("jQuery21105429139183596063_1547264955666("):-1]

        res_dict = json.loads(json_s)

        tasks = []
        for idx, item in enumerate(res_dict['programs']):
            fname = '/Users/mz/Downloads/感受北京.' + item['file_name'][-8:] + '.mp4'
            stream_url = item['file_streaming']
            tasks.append(asyncio.ensure_future(download_stream(fname, stream_url)))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        start += size
        print("start =========== %s" % start)
        if len(res_dict.get('programs', [])) == 0:
            break



if __name__ == '__main__':
    print('start')
    s = time.time()
    run()
    e = time.time()
    print('end')
    print(e-s)


