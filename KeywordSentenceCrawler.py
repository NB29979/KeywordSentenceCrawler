# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import chardet


proxy_dict = {
    "http":"http://ctwc0162:a6Mj7Wh6K@proxy.doshisha.ac.jp:8080/",
    "https":"https://ctwc0162:a6Mj7Wh6K@proxy.doshisha.ac.jp:8080/"
}


def access_url(_url, _depth):
    if _depth > 3:
        return

    print('accessed: '+_url)
    html = requests.get(_url, proxies=proxy_dict).content

    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', text=re.compile('。$'))
    for div in divs:
        print(div.get_text())

    # todo: テキストの抽出,保存
    # todo: 見つかった<link>だけのstackを用意
    # todo: stack.pop()してaccessed_urlsに存在しなければ.top()のurlをaccessed_urlsに追加，access_url(_url, _depth+1)


# アクセス予定のルートurlスタック
root_links = open('root_links', 'r')
url_stack = list(set(root_links.readlines()))

accessed_urls = []
for i in range(len(url_stack)):
    url = url_stack[-1]
    url_stack.pop()
    access_url(url, 1)