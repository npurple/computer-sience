from bs4 import BeautifulSoup
import requests
from pprint import pprint

def grab(i, url):
    r = requests.get(url, timeout=None)
    soup = BeautifulSoup(r.content, "lxml")
    # print(dir(soup))
    # print(soup.prettify)
    title = soup.h1.text
    cnt = soup.find(id='content')
    text = cnt.text
    content = '\n'.join([title, text])
    with open('fendou/%s.txt' % title, 'w') as f:
        f.write(content)
    

def main():
    tid = 8337842
    for i in range(63):
        url = 'http://www.597txt.com/files/article/html/22/22678/%s.html' % tid
        grab(i, url)
        tid += 1


main()

