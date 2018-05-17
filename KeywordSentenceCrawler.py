# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import chardet
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def access_url(_url, _depth):
    if _depth > 3:
        return

    driver.get(_url)
    visited_sites.append(_url)

    result = driver.find_element_by_tag_name('div').text
    with open('web_page_texts', 'a') as output:
        output.writelines(result)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=re.compile('html$'))]
    print(links)
    print('by: '+_url)

    # todo: テキストの抽出,保存
    # todo: 見つかった<link>だけのstackを用意
    # todo: stack.pop()してvisited_urlsに存在しなければ.top()のurlをaccessed_urlsに追加，
    # access_url(_url, _depth+1)


driver = webdriver.Chrome()

# アクセス予定のルートurlスタック
root_links = open('root_links', 'r')
url_stack = list(set(root_links.readlines()))
visited_sites = []

access_url('http://www.doshisha.ac.jp/information/campus/access/shinmachi.html',1)

for i in range(len(url_stack)):
    url = url_stack[-1]
    url_stack.pop()
    access_url(url, 1)

driver.close()
