# coding=utf8
import os
import re
import time
from bs4 import BeautifulSoup
import requests
# import docx
from pprint import pprint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/21cn_books", max_overflow=5)
Base = declarative_base()
Session = sessionmaker(engine)
db_sessioin = Session()

# 创建单表
class Yuwen(Base):
    __tablename__ = 'yuwen'
    id = Column(Integer, primary_key=True)
    grade = Column(String(16))
    version = Column(String(32))
    volume = Column(String(32))
    title = Column(String(32))
    text = Column(Text)


export_dir = '/Users/mz/lab/study/crawler/yuwen'
def export():
    for obj in db_sessioin.query(Yuwen).order_by(Yuwen.id): 
        # print(obj)
        # print(obj.grade, obj.version, obj.volume, obj.title, obj.text)
        path = '/'.join([export_dir, obj.grade, obj.version])
        try:
            os.makedirs(path)
        except FileExistsError as fee:
            # print(fee)
            pass
        except Exception as e:
            print(e)
            continue
        if not obj.title:
            continue
        doc = '/'.join([path, obj.volume]) + '.txt'
        print(doc)
        try:
            with open(doc, 'a+') as f:
                f.write(obj.title)
                f.write('\n')
                f.write(clear_noise(obj.text))
                f.write('\n' * 3)
        except Exception as e:
            print(e)
            continue

def clear_noise(src):
    pattern = re.compile(r'【更多推荐】.*')
    dst = re.sub(pattern, '', src)
    # print(dst)
    return dst

def save_gbk():
    pass

def save_utf8():
    pass

def save_word():
    pass

host = "https://www.21cnjy.com"
def lessons_degree(volume_url, grade, version, volume):
    """
        return: {}
    """
    # print('get_lessons______________%s' % volume_url)
    r = requests.get(volume_url, timeout=None)
    soup = BeautifulSoup(r.content, "lxml")
    chapters = soup.find(class_='chapter-list')
    contents = chapters.find_all(class_='chapter-name')
    for content in contents:
        title = content.text
        text_url = host + content.find('a').get('href').strip()
        text_r = requests.get(text_url, timeout=None)
        text_soup = BeautifulSoup(text_r.content, "html.parser", from_encoding='gbk')
        lines = text_soup.find(class_='article').stripped_strings
        lines = []
        for line in text_soup.find(class_='article').stripped_strings:
            lines.append(line)
        text = "\n".join(lines)
        # print('#-'*10 + "\n")
        # print(grade, version, volume, title, text)
        obj = Yuwen(grade=grade, version=version, volume=volume, title=title, text=text)

        db_sessioin.add(obj)

    db_sessioin.commit()


# the version detail in all of versions in (小学，初中，高中)
def volume_degree(url, grade, version):
    r = requests.get(url, timeout=None)
    version_detail_soup = BeautifulSoup(r.content, "lxml")
    tree = version_detail_soup.find(class_='tree')
    for a in tree.find_all('a'):
        href = a.get('href').strip()
        volume = a.text.strip()
        url = host + href
        if href.split('/')[-2] != '0':
            lessons_degree(url, grade, version, volume) 
            # break


def main():
    url = "https://www.21cnjy.com/yuwen/kewen/"
    r = requests.get(url, timeout=None)
    soup = BeautifulSoup(r.content, "lxml")
    kNav = soup.find(id="kNav")
    grades = kNav.find_all('a')
    subList = soup.find(id="subList")
    versions_of_grade = subList.find_all(class_='filter-col')
    for grade, versions in zip(grades, versions_of_grade):
        # print('*-'*10)
        for version in versions.find_all('a'):
            # print(i, grade.text, version.text)
            # continue
            href = version.get('href').strip()
            url = host + href
            volume_degree(url, grade.text, version.text)
            # print(lessons)


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    # main()
    # create_table()
    export()
    sample = """
        “不是她们是谁，一群落后分子！”说完把纸盒顺手丢在女人们船上，一泅，又沉到水底下去了，到很远的地方才钻出来。
小队长开了个玩笑，他说：
“你们也没有白来，不是你们，我们的伏击不会这么彻底。可是，任务已经完成，该回去晒晒衣裳了。情况还紧的很！”战士们已经把打捞出来的战利品，全装在他们的小船上，
准备转移。一人摘了一片大荷叶顶在头上，抵挡正午的太阳。几个青年妇女把掉在水里又捞出来的小包裹，丢给了他们，战士们的三只小船就奔着东南方向，箭一样飞去了。不久就消失在中午水面上的烟波里。
几个青年妇女划着她们的小船赶紧回家，一个个像落水鸡似的。一路走着，因过于刺激和兴奋，她们又说笑起来，坐在船头脸朝后的一个噘着嘴说：
“你看他们那个横样子，见了我们爱搭理不搭理的！”
“啊，好像我们给他们丢了什么人似的。”
她们自己也笑了，今天的事情不算光彩，可是：
“我们没枪，有枪就不往荷花淀里跑，在大淀里就和鬼子干起来！”
“我今天也算看见打仗了。打仗有什么出奇，只要你不着慌，谁还不会趴在那里放枪呀！”
“打沉了，我也会凫水捞东西，我管保比他们水式好，再深点我也不怕！”
“水生嫂，回去我们也成立队伍，不然以后还能出门吗！”
“刚当上兵.........谁比谁落后多少呢！”
这一年秋季，她们学会了射击。冬天，打冰夹鱼的时候，她们一个个登在流星一样的冰船上，来回警戒。敌人围剿那百亩大苇塘的时候，她们配合子弟兵作战，出入在那芦苇的海里。
【更多推荐】人教版第二册语文全册课文
内容为空！
    """
    # clear_noise(sample)
