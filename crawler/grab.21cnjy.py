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

def get_lessons(volume_url):
    """
        return: {}
    """
    print('get_lessons______________%s' % volume_url)
    r = requests.get(volume_url)
    soup = BeautifulSoup(r.content, "lxml")
    chapters = soup.find(class_='chapter-list')
    contents = chapters.find_all(class_='chapter-name')
    lessons = {}
    for content in contents:
        # print(content)
        title = content.text
        text_url = host + content.find('a').get('href').strip()
        # print(text_url)
        text_r = requests.get(text_url)
        text_soup = BeautifulSoup(text_r.content, "html.parser", from_encoding='gbk')
        print('stripped_strings' in dir(text_soup))
        print('stripped_strings' in dir(text_soup.find(class_='article')))
        print('stripped_strings' in dir(text_soup.find(class_='article').get_text))
        lines = text_soup.find(class_='article').stripped_strings
        lines = []
        for line in text_soup.find(class_='article').stripped_strings:
            lines.append(line)
        text = "\n".join(lines)

        # text = text_soup.find(class_='article').get_text()
        # print(type(article), dir(article))
        # article.replace('<br/>', '')
        # article.replace(r'\n', '\n')
        # article.replace(r'\u3000', u' ')
        # article.replace(u'\xa0', u'').encode('utf-8')
        # article = "".join(article.split())
        print('================')
        print(text)
        # print(text_url)
        # print(article)
        # text.replace()
        # text.replace(u'\xa0', u' ').strip().encode('utf-8')
        # text.replace(u'\u3000', u' ').strip().encode('utf-8')
        lessons[title] = text
        # pprint(lessons)
        f = open('./tmp/%s' % title, 'w')
        f.write(text)
        f.close()
    # print(lessons)
    return lessons

    

# the version detail in all of versions in (小学，初中，高中)
def fill_version_detail(url, fill_map):
    # version_map = {}
    r = requests.get(url)
    version_detail_soup = BeautifulSoup(r.content, "lxml")
    # print(version_detail_soup.prettify())
    tree = version_detail_soup.find(class_='tree')
    # print(type(tree), tree)
    
    parent = None
    for a in tree.find_all('a'):
        href = a.get('href').strip()
        text = a.text.strip()
        url = host + href
        # print(href, text)
        # print(href.split('/'))
        if href.split('/')[-2] == '0':
            parent = text
            if parent not in fill_map:
                fill_map[parent] = {'name': text, 'url': url}
        else:
            fill_map[parent][text] = {'name': text, 'url': url}
            lessons = get_lessons(url) 
            fill_map[parent][text]['lessons'] = lessons
            break


def main():
    url = "https://www.21cnjy.com/yuwen/kewen/"
    r = requests.get(url)
    # print(r.status_code, r.content)
    soup = BeautifulSoup(r.content, "lxml")
    # print(soup.prettify())
    kNav = soup.find(id="kNav")
    # print(kNav)
    for x in kNav.find_all('a'):
        # print(x.text)
        pass
    subList = soup.find(id="subList")
    # print(subList)
    # print(type(subList), dir(subList))
    # print('\n'*2)
    # for x in subList.find_all(class_='subjectList'):
    version_detail_map = {}
    for grade in subList.find_all(class_='filter-col'):
        # print(grade)
        # print('\n')
        i = 0
        for version in grade.find_all('a'):
            i+=1
            if i==1:
                continue
            # print(version.text)
            # print(version)
            href = version.get('href').strip()
            url = host + href
            fill_version_detail(url, version_detail_map)
            if i == 3:
                break
        break
    # pprint(version_detail_map)


if __name__ == '__main__':
    main()
    # get_lessons('https://www.21cnjy.com/yuwen/kewen/1/2/73938/73943/')
