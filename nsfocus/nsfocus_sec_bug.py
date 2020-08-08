import requests
import re
import time
import pymysql
from pyquery import PyQuery as pq

baseurl = 'http://www.nsfocus.net/index.php?act=sec_bug&type_id=&os=&keyword=&page='

def get_HTML(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Content-Type': 'application/json; charset=utf-8'}
    cookies = {'Cookies': 'your cookie'}
    html = requests.post(url, headers=headers, cookies=cookies)
    html.encoding = html.apparent_encoding
    return html.text

conn = pymysql.connect(
    host="127.0.0.1",
    user="root", password="123456",
    database="apsecheduler",
    charset="utf8"
)

cursor = conn.cursor()


for i in range(1,100):
    url = baseurl + str(i)
    print(url)
    html = get_HTML(url)
    html2 = pq(html)
    content = html2('div').find('.vul_list')
    print(content.text())
    time.sleep(5)