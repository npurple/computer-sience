# coding=utf8
import time
from bs4 import BeautifulSoup
import requests
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

        # f = open('./tmp/%s' % title, 'w')
        # f.write(text)
        # f.close()
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
        i = 0
        for version in versions.find_all('a'):
            i+=1
            if i==1:
                continue
            # print(i, grade.text, version.text)
            href = version.get('href').strip()
            url = host + href
            volume_degree(url, grade.text, version.text)
            # print(lessons)
            # if i == 2:
            #     break
        # break


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
    # create_table()
    '''
    with open('/tmp/sleep.txt', 'w+') as f:
        i = 0
        while 1:
            cnt = "%s\n" % i
            print(cnt)
            f.write(cnt)
            i += 1
            time.sleep(2)
            if i == 50:
                break
    '''

