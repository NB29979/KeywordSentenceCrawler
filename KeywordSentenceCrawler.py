# coding: utf-8
from bs4 import BeautifulSoup
import re
import codecs
from selenium import webdriver


def access_url(_url, _depth):
    if _depth > 3:
        return
    if _url in visited_sites:
        return

    driver.get(_url)
    visited_sites.append(_url)

    # webページのテキストの抽出とファイル出力
    result = driver.find_element_by_tag_name('div').text
    with codecs.open('web_page_texts', 'a', 'cp932', 'ignore') as output:
        output.writelines(result)

    # リンクを探して踏む
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a', href=re.compile('html$'))]

    for link in links:
        if link[0] == '/':
            print('part: '+link)

    print(links)
    print('by: '+_url)

    # todo: 見つかった<link>だけのstackを用意
    # todo: stack.pop()してvisited_urlsに存在しなければ.top()のurlをaccessed_urlsに追加，
    # access_url(_url, _depth+1)


driver = webdriver.Chrome()

# アクセス予定のルートurlスタック
root_links = open('root_links', 'r')
url_stack = list(set(root_links.readlines()))
visited_sites = []

for i in range(len(url_stack)):
    url = url_stack[-1]
    url_stack.pop()
    access_url(url, 1)

driver.close()
