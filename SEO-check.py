import sys
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import pandas as pd
from multiprocessing import Pool

target = 'https://www.maedakosen.jp/'

def get_search_html(keyword):
    # start = "&start=" + str(page * 10) # 次ページstart=10
    # https://www.google.co.jp/search?hl=ja&num=100&q=%E8%83%BD%E7%99%BB%E5%8D%B0%E5%88%B7
    url = 'https://www.google.co.jp/search?hl=ja&num=50&q=' + quote(keyword)
    # url = 'https://www.google.com/search?q=' + quote(keyword) + start 
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"

    headers = {'User-Agent': user_agent}

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as res:
        body = res.read()
        return body


def get_page_rank(soup):
    res_rank = 1

    for a_tag in soup.find_all('a'):
        h3_tag = a_tag.select("h3")

        if len(h3_tag) > 0:
            if a_tag.get('href').startswith(target) == True:
                # print(h3_tag[0].get_text())
                # print(a_tag.get('href'))
                return res_rank

            res_rank += 1
    return -1

def acsess(keyword):
    rank = -1

    #for page in range(max_page):
    html = get_search_html(keyword)
    soup = BeautifulSoup(html, 'html.parser')

    title_text = soup.find('title').get_text()
    print(title_text)
    rank = get_page_rank(soup)

    # time.sleep(1) # アクセス制限対策
        
    if rank != -1:
        rank
    else:
        rank = "圏外"
    return rank

if __name__ == "__main__":

    keyword = ['ネイチャーネット','ジオフリース','汚濁防止フェンス','パワフルユニット']
    # 並列化する数
    # 通常は2-4までだが今回の場合は使わない方がいい
    pool = Pool(4)
    # ループする回数
    ranks = pool.map(acsess, keyword)

    for rank in ranks:
        print(rank)
    