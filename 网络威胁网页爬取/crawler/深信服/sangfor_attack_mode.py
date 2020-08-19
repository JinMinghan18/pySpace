import requests
from pyquery import PyQuery as pq
import time
import MySQLdb
import json

def getHTML(url,form_data):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    html = requests.get(url,params = form_data,headers=header)
    print(html.request.url)
    html.encoding = html.apparent_encoding
    return html.text

url = "https://sec.sangfor.com.cn/api/v1/vuln_wiki/get_attack_list"

json_data={
    "search_field": "",
    "vuln_level": "",
    "vuln_type": "",
    "start_time": "",
    "end_time": "",
    "page_index": 1,
    "page_size": 60,
    "sort_order": -1,
    "sort_field": "vuln_discover_date"
}

db = MySQLdb.connect('localhost','root','123456','crawler',charset='utf8')
cursor = db.cursor()

for i in range(2):

    json_data["page_index"] = i+1
    html = getHTML(url,json_data)
    res = json.loads(html)["data"]
    sql = "Insert Into sangfor_attack_mode Values\n"

    for it in res:
        tmp = "("
        for it2 in it:
            if type(it[it2]) is int:
                tmp = tmp + str(it[it2]) + ","
            elif type(it[it2]) is str:
                tmp = tmp + "'" + it[it2].replace("'","\\'") + "',"

        tmp = tmp[0:len(tmp)-1] + "),\n"
        sql = sql + tmp
        # break

    sql = sql[0:len(sql)-2]

    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("Failed to insert db")
        
    print("第{}页已经爬取到数据库".format(i+1))
    time.sleep(10)
    print("睡眠结束")

db.close()