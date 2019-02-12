# coding=utf8


import requests
import datetime

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import mail_cfg
import time

remain = 100
host = 'https://gugong.228.com.cn'
api = 'ImmersionDigitalExperienceExhibition/GetOutVenueData'
headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "https://gugong.228.com.cn",
        "Referer": "https://gugong.228.com.cn/ImmersionDigitalExperienceExhibition/SelectPrice",
        "Cookie": "ASP.NET_SessionId=uxunxxbi4d4sqg4day4eeoti; NTKF_T2D_CLIENTID=guestA23B2910-6133-169A-42D4-AC11E1EED3A3; MyCook=UserName=18618364050; YSMyCookie=ylsid=uxunxxbi4d4sqg4day4eeoti; nTalk_CACHE_DATA={uid:kf_9209_ISME9754_guestA23B2910-6133-16,tid:1549941719237558}; Hm_lvt_03aa38430f8c7b8e004251a9f67c2183=1549075080,1549262391,1549262564,1549941719; Hm_lpvt_03aa38430f8c7b8e004251a9f67c2183=1549941773",
        "X-Requested-With": "XMLHttpRequest",
    }


def plus_date(days):
    return plus_date_from(datetime.datetime.today().date(), days)


def plus_date_from(from_date, days):
    return from_date + datetime.timedelta(days)


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
    response = requests.post(url, data, headers=headers, timeout=timeout)
    return response.json()


def tickets_of_date(date):
    date_str = date.strftime('%Y-%m-%d')
    payload = {'date': date_str}
    resp = http_post(host, api, headers, payload)
    range_count = 0
    current_remain = 0
    for t in resp['Result']:
        range_count += 1
        range_name = t['Name']
        remain_of_range = t['TotalRemain']
        print(range_name, remain_of_range)
        current_remain += remain_of_range

    if 0 < current_remain < remain * range_count:
        # print("selling, go and buy it")
        remind_msg = 'ticket of gugong show of %s is selling now, plz go buy it' % date_str
        remind(remind_msg)


def remind(msg):
    sender = mail_cfg.mail_from
    receivers = ['mz1985@163.com']
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = mail_cfg.mail_from
    message['To'] = "mz1985@163.com"
    message['Subject'] = 'gugong yuding'
    try:
        server = smtplib.SMTP('smtp.163.com', 25)
        server.set_debuglevel(1)
        server.login(mail_cfg.mail_from, mail_cfg.pwd)
        server.sendmail(sender, receivers, message.as_string())
    except smtplib.SMTPException:
        pass
    finally:
        server.quit()


def run_forever():
    while True:
        for i in range(2, 5):
            dst = plus_date(i)
            tickets_of_date(dst)
        time.sleep(60)


if __name__ == '__main__':
    run_forever()
