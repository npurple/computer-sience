# coding=utf8
import os
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


export_dir = '/Users/mz/lab/study/crawler/yuwen'
def export():
    for obj in db_sessioin.query(Yuwen).order_by(Yuwen.id): 
        # print(obj)
        # print(obj.grade, obj.version, obj.volume, obj.title, obj.text)
        path = '/'.join([export_dir, obj.grade, obj.version, obj.volume])
        try:
            os.makedirs(path)
        except FileExistsError as fee:
            print(fee)
        except Exception as e:
            print(e)
            continue
        if not obj.title:
            continue
        doc = '/'.join([path, obj.title])
        print(doc)
        try:
            with open(doc, 'w') as f:
                f.write(obj.text)
        except Exception as e:
            print(e)
            continue



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
