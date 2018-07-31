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
    if _url not in root_links:
        visited_sites.append(_url)

    # webページのテキストの抽出とファイル出力
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for s in soup(['script', 'style']):
        s.decompose()
    result = '\n'.join(soup.stripped_strings)
    with codecs.open('web_page_texts', 'a', 'cp932', 'ignore') as output:
        output.writelines(result)

    # リンクを探して踏む
    links = [link.get('href') for link in soup.find_all('a', href=re.compile(r'.*/+.'))]
    links_ = [link for link in links if not re.match(r'pdf$', link)]
    domain = re.search(r'http(.+)((.jp)|(na.be)|(.net)|(.com)|(.info))', _url)
    links_in_site = []

    for link in links_:
        if link and link[0] == '/' or '..' in link:
            links_in_site.append(domain.group(0)+link)

    for i in range(len(links_in_site)):
        link = links_in_site[-1]
        links_in_site.pop()
        try:
            access_url(link, _depth+1)
        except:
            continue

    print(_url)


driver = webdriver.Chrome()

# アクセス予定のルートurlスタック
root_links = open('root_links', 'r')
url_stack = list(set(root_links.readlines()))
visited_sites = []

for i in range(len(url_stack)):
    url = url_stack[-1]
    print('root:'+url)
    url_stack.pop()
    access_url(url, 1)

driver.close()
