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
guodanian_api = 'ImmersionDigitalExperienceExhibition/GetOutVenueData'
yuanxiao_api = 'ShangyuanNight/GetOutVenueData'
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

def tickets_of_shangyuanye(date):
    """
        “紫禁城上元之夜”
        在2019己亥年元宵节来临之际故宫博物院将于2019年2月19日(正月十五)、20日（正月十六）举办“紫禁城上元之夜”文化活动。活动地点主要安排在故宫博物院的午门展厅、太和门广场、故宫东城墙、神武门等区域，此活动最后经神武门退场。观众朋友需通过故宫博物院票务系统预约此项活动，免费参加，名额有限，约满为止。故宫预约实行实名制，所有观众需录入身份证或护照信息方可预定。预约成功的观众从午门凭身份证安检入场。网上预约信息仅限本人使用，不得转借于他人，参观时请务必携带好身份证件。
        下单时填写了二代身份证号的观众可在入院日当日持身份证或户口本原件在任意检票口直接入院，无须兑换纸质门票。
        多人订单在验票时，任意一人验票成功后，订单内所有观众均视为已验票（已验票则无法申请退款），但其他人仍须出示证件进行二次验票。
        每人每天可预约一次，且不可更改。


        预约须知
            1、“紫禁城上元之夜”开放预约时间：
                正午十五（2月19日）于2月17日开放预约
                正月十六（2月20日）于2月18日开放预约
            2、本预约参观范围只包含“紫禁城上元之夜”文化活动，需要通过网上预约才可参加此项活动。每个证件（身份证/护照）限预约一张上元之夜门票。
            3、预约门票时填写了二代身份证号的观众可在入院日当日持身份证或户口本原件在故宫午门西侧（1—12号检票口）任意检票口直接入院，无需兑换纸质门票。
            4、多人订单在验票时，任意一人验票成功后，订单内所有观众均视为已验票，但其他人仍须出示证件进行二次验票。
            5、身高达到1米2以上的儿童需预约，身高未达到1米2的儿童无需单独预约，仅家长预约即可。12岁以下儿童须至少有一名家长陪同，家长需预约。
            6、特殊人群（军人、残疾人、老年人、离退休干部）均需网上预约。
            7、请严格按照预约时段入场参观，避免出现过早的提前到场或者迟到的情况，未能按照预约时间到场的观众将视为自动放弃参观，第一批预约观众在18:30开始检票入场，第二批预约观众在19:00开始检票入场，第三批观众在19:30开始检票入场，当晚20时停止入场，工作人员将根据当日场次的实际参观人数进行调整，请听从安排。
            8、因故宫博物院无停车场所，为了观众能有更好的参观体验，故不建议观众驾车前来参观，敬请谅解。
            9、请遵守参观规定，听从工作人员疏导，内部光线较暗，请注意自身和他人的人身安全，切勿大声喧哗、打闹、跑跳。
            10、请配合入院安检。食品、液体、火源、易燃、易爆、自拍杆等物品，以及一切危害公共安全的违禁物品禁止带入。上元之夜不具备存包条件，大型行李箱包（宽40cm，高30cm以上）谢绝入内。
            11、请爱护宫内设备和设施，勿用力拍打宫内设施，勿用尖锐物品刻画墙面，勿将宫内任何物品带出。
    """
    date_str = date.strftime('%Y-%m-%d')
    payload = {'date': date_str}
    resp = http_post(host, yuanxiao_api, headers, payload)
    time_ranges = resp['Result']
    for period in time_ranges:
        sid = period['SId']
        if int(sid) == 5237:  # 19:30入场
            print(period)
            remain = period['TotalRemain']
            print(remain)
            if int(remain) <= 800:
                remind('快去故宫官网抢票（上元夜）网址：https://gugong.228.com.cn/ShangyuanNight/SelectPrice')


def tickets_of_guodanian(date):
    date_str = date.strftime('%Y-%m-%d')
    payload = {'date': date_str}
    resp = http_post(host, guodanian_api, headers, payload)
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
        # 故宫过大年
        for i in range(2, 5):
            dst = plus_date(i)
            tickets_of_guodanian(dst)

        # 上元夜
        dst = datetime.datetime(2019, 2, 20)
        tickets_of_shangyuanye(dst)
        time.sleep(30)


if __name__ == '__main__':
    run_forever()
