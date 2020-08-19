import requests
from pyquery import PyQuery as pq
import json
import MySQLdb
import time

def getHTML(url,params):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    html = requests.get(url,headers=headers,params=params,stream=True)
    html.encoding = html.apparent_encoding
    return html.text

params={
    "page_size": 60,
    "page_index": 1,
    "category": '["all"]',
    "query_string": ""
}

url = "https://sec.sangfor.com.cn/api/v1/wiki_events/query_many_wiki_event"

db = MySQLdb.connect('localhost','root','admin','crawler',charset='utf8')
cursor = db.cursor()
errortxt = open('error.txt','w+',encoding='utf-8')

for i in range(7):

    params['page_index'] = i+1
    html = getHTML(url,params)
    with open("tmp.txt",'w+',encoding='utf-8') as f:
        f.write(html)
    break
    res = json.loads(html)['data']
    sql = "Insert Into sangfor_security_events Values\n"

    for it in res:
        tmp = "("
        for it2 in it:
            tmp = tmp + "'" + it[it2].replace("'","\\'") + "',"

        tmp = tmp[0:len(tmp)-1] + "),\n"
        sql = sql + tmp

    sql = sql[0:len(sql)-2]
    
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("Failed to insert db")
        errortxt.write(sql)
        
    print("第{}页已经爬取到数据库".format(i+1))
    time.sleep(10)
    print("睡眠结束")

errortxt.close()
db.close()