import requests
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup
from pykakasi import kakasi
import re

#webページを取得して解析する(企業情報)
load_url = "https://job.rikunabi.com/2021/company/r357600054/"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
souptexts = soup.text

#メール
chap04 = None
for mailtext in souptexts.split("\n"):
    if re.search(r'[\w\.-]+@[\w\.-]+', mailtext):
        chap04 = re.search(r'[\w\.-]+@[\w\.-]+', mailtext)
        chap04 = chap04.group(0)
        break
    else:
        chap04 = None

print(chap04)

#URL
chap05 = None
for urltext in souptexts.split("\n"):
    if re.search(r'https?://[^/]+', urltext):
        chap05 = re.search(r'https?://[^/]+', urltext)
        chap05 = chap05.group(0) + "/"
        break
    else:
        chap05 = None

if chap05 == "https://job.mynavi.jp/":
    chap05 = None

print(chap05)

#URL パート2
chap06 = None
chap06 = soup.find(id="corpDescDtoListDescText120")
if chap06 != None:
    chap06 = chap06.text
print(chap06)