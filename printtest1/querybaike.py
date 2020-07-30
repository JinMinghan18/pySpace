import re
import urllib
from quopri import quote

import requests
import time
import datetime
import pandas as pd
from pyquery import PyQuery as pq

url1='http://baike.baidu.com/item/'
urls = []
urls.append("乐清")
urls.append("杭州")

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6776.400 QQBrowser/10.3.2601.400'}
country_locations=[]
country_name2 = []
country_urls=[]
baseurl=[]
baseurl.append(url1+urls[0])
baseurl.append(url1+urls[1])


try:
    start = datetime.datetime.now()
    #request实现http请求
    county_context = requests.get(baseurl[0],timeout=10,headers=header)
    county_context.encoding='utf-8'
    doc = pq(county_context.text)
    content = doc.find(".main-content")

    f = open('file1.txt', 'a+', encoding='utf-8')
    for item in content.children().items():
        if(item.attr('class') == 'lemma-summary'):
            div = item.find('div')
            context_summary ="概况\n" + div.text()
            print(context_summary)
            f.write(context_summary)
    comp_loca = re.compile(
        '.*?地理环境.*?地理环境.*?(.*?)乐清自然资源',
        re.S)
    county_loca = re.findall(comp_loca, content.text())
    country_locations.extend(county_loca)
    county_locastr = "".join(county_loca)  # list转str
    print(county_locastr)
    county_locastr = county_locastr.replace('编辑', ' ')

    f.write(county_locastr)
finally:
    print('end')