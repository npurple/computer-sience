# coding=utf8
from bs4 import BeautifulSoup
import requests
from pprint import pprint

'''
example:

url = "https://movie.douban.com/chart"
r = requests.get(url)
soup = BeautifulSoup(f.content, "lxml")

for k in soup.find_all('div',class_='pl2'):
   a = k.find_all('span')
   print(a[0].string)

'''
host = "https://www.21cnjy.com"

def lessons_degree(volume_url, grade, version, volume):
    """
        return: {}
    """
    # print('get_lessons______________%s' % volume_url)
    r = requests.get(volume_url)
    soup = BeautifulSoup(r.content, "lxml")
    chapters = soup.find(class_='chapter-list')
    contents = chapters.find_all(class_='chapter-name')
    lessons = {}
    for content in contents:
        title = content.text
        text_url = host + content.find('a').get('href').strip()
        text_r = requests.get(text_url)
        text_soup = BeautifulSoup(text_r.content, "html.parser", from_encoding='gbk')
        lines = text_soup.find(class_='article').stripped_strings
        lines = []
        for line in text_soup.find(class_='article').stripped_strings:
            lines.append(line)
        text = "\n".join(lines)
        print('#-'*10 + "\n")
        print(grade, version, volume, title, text)
        # f = open('./tmp/%s' % title, 'w')
        # f.write(text)
        # f.close()

    

# the version detail in all of versions in (小学，初中，高中)
def volume_degree(url, grade, version):
    r = requests.get(url)
    version_detail_soup = BeautifulSoup(r.content, "lxml")
    tree = version_detail_soup.find(class_='tree')
    
    parent = None
    for a in tree.find_all('a'):
        href = a.get('href').strip()
        volume = a.text.strip()
        url = host + href
        if href.split('/')[-2] != '0':
            lessons = lessons_degree(url, grade, version, volume) 
            break


def main():
    url = "https://www.21cnjy.com/yuwen/kewen/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    kNav = soup.find(id="kNav")
    grades = kNav.find_all('a')
    subList = soup.find(id="subList")
    versions_of_grade = subList.find_all(class_='filter-col')
    for grade, versions in zip(grades, versions_of_grade):
        print('*-'*10)
        i = 0
        for version in versions.find_all('a'):
            i+=1
            if i==1:
                continue
            href = version.get('href').strip()
            url = host + href
            volume_degree(url, grade.text, version.text)
            print(lessons)
            if i == 2:
                break
        break


if __name__ == '__main__':
    main()
