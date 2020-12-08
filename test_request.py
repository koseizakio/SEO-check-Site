from flask import *
import sys
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import datetime
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
            start2 = time.time()

            def get_search_html(keyword):
                # start = "&start=" + str(page * 10) # 次ページstart=10
                # https://www.google.co.jp/search?hl=ja&num=100&q=%E8%83%BD%E7%99%BB%E5%8D%B0%E5%88%B7
                url = 'https://www.google.co.jp/search?hl=ja&num=50&q=' + quote(keyword)
                # url = 'https://www.google.com/search?q=' + quote(keyword) + start 
                
                headers = {'User-Agent': user_agent}

                req = urllib.request.Request(url, headers=headers)

                with urllib.request.urlopen(req) as res:
                    body = res.read()
                    return body

            def get_page_rank(soup):
                res_rank = 1

                # if re.search(target,soup.find_all('a').text) == None:
                #     return -1
                    
                for a_tag in soup.find_all('a'):

                    h3_tag = a_tag.select("h3")

                    if len(h3_tag) > 0:
                        if a_tag.get('href').startswith(target) == True:
                            # print(h3_tag[0].get_text())
                            # print(a_tag.get('href'))
                            return res_rank

                        res_rank += 1
                return -1

            for keyword in keywords:
                rank = -1
                start = time.time()
                #for page in range(max_page):
                html = get_search_html(keyword)
                soup = BeautifulSoup(html, 'html.parser')
                    
                title_text = soup.find('title').get_text()
                print(title_text)
                rank = get_page_rank(soup)
                    
                if rank != -1:
                    ranks.append(rank)
                else:
                    rank = "圏外"
                    ranks.append(rank)
                print(ranks)

                # アクセス制限対策(1-3)
                # 明日は、10秒くらいあける
                time.sleep(5)
                elapsed_time = time.time() - start
                print(elapsed_time)

            elapsed_time2 = time.time() - start2
            print(elapsed_time2)

            return render_template('ranks.html', ranks=ranks, keynote=keynote, target=target)
        else:
            return abort(400)
    except Exception as e:
        return render_template('error.html', error=e)

@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error=e)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
