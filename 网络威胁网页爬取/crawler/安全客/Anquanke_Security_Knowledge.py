import requests
from pyquery import PyQuery as pq
import time
import MySQLdb
import json


def getHTML(url, params):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
    html = requests.get(url, params=params, headers=headers)
    html.encoding = html.apparent_encoding
    # print(html.status_code)
    # print(html.url)
    return html.text


params = {"page": "3",
          "size": "10",
          "category": "knowledge"}

url = "https://api.anquanke.com/data/v1/posts"

db = MySQLdb.connect('localhost', 'root', 'admin','crawler', charset='utf8')
cursor = db.cursor()
errortxt = open('anquanke-error.txt', 'w+', encoding='utf-8')

for i in range(10):
    params["page"] = i + 1

    html = getHTML(url, params)

    res = json.loads(html)["data"]

    sql = "Insert Into Anquanke_Security_Knowledge Values"
    for it in res:

        _id = it["id"]
        title = it["title"].replace("'","\\'")
        desc = it["desc"].replace("'","\\'")
        date = it["date"].replace("'","\\'")
        img = it["cover"].replace("'","\\'")
        tags = ""
        for tag in it["tags"]:
            tags = tags + tag + "/"

        tags = tags[0:len(tags)-1].replace("'","\\'")
        author = it["author"]
        nickname = author["nickname"].replace("'","\\'")

        sql = sql + "(" + str(_id) + ",'" + title + "','" + desc + "','" + date + "','" + img + "','" + tags + "','" + nickname + "'),\n"

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
