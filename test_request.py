from flask import *
import sys
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import re

app = Flask(__name__)

#ランキング格納
ranks = []
text = None

#最初のスタート
@app.route('/')
def index():
	return render_template('index.html')

#ポストされたら
@app.route('/test', methods=['POST'])
def test():
    try:
        if request.method == 'POST':
            keywords = request.form['keyword']
            keynote = keywords
            target = request.form['url']
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
            ranks = []
            keywords = re.split('\n', keywords)

            for keyword in keywords:

                def get_search_html(keyword, page):
                    start = "&start=" + str(page * 10) # 次ページstart=10
                    #https://www.google.co.jp/search?hl=ja&num=100&q=%E8%83%BD%E7%99%BB%E5%8D%B0%E5%88%B7
                    # url = 'https://www.google.co.jp/search?hl=ja&num=50&q=' + quote(keyword)
                    url = 'https://www.google.com/search?q=' + quote(keyword) + start 
                    
                    headers = {'User-Agent': user_agent}

                    req = urllib.request.Request(url, headers=headers)

                    with urllib.request.urlopen(req) as res:
                        body = res.read()
                        return body


                def get_page_rank(soup, page):
                    res_rank = 1

                    for a_tag in soup.find_all('a'):
                        h3_tag = a_tag.select("h3")

                        if len(h3_tag) > 0:
                            if a_tag.get('href').startswith(target) == True:
                                # print(h3_tag[0].get_text())
                                # print(a_tag.get('href'))
                                return res_rank + page * 10

                            res_rank += 1
                    return -1

                rank = -1
                max_page = 5

                for page in range(max_page):
                    html = get_search_html(keyword, page)
                    soup = BeautifulSoup(html, 'html.parser')

                    title_text = soup.find('title').get_text()
                    print(title_text)
                    rank = get_page_rank(soup, page)

                    page += 1
                    if rank != -1:
                        break

                    # time.sleep(1) # アクセス制限対策
                    

                if rank != -1:
                    ranks.append(rank)
                else:
                    rank = "圏外"
                    ranks.append(rank)
                print(ranks)


            return render_template('ranks.html', ranks=ranks, keynote=keynote, target=target)
        else:
            return abort(400)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()