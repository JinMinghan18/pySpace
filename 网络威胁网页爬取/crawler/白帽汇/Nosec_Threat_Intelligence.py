import requests
from pyquery import PyQuery as pq
import time
import MySQLdb
import json

url = "https://nosec.org/home/index/threaten.html"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
session = requests.session()

html = session.get(url, headers=headers)

html.encoding = html.apparent_encoding
print(html.status_code)
print(html.request.headers)
print(html.reason)
print(html.url)
print("\n")
print(html.headers)

doc = pq(html.text)

token = doc("[name=csrf-token]").attr("content")

print(token)
print(session.cookies)

url = "https://nosec.org/home/ajaxindexdata"

params = {"keykind": "threaten",
          "page": 1}

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-CSRF-TOKEN": token,
        "X-Requested-With": "XMLHttpRequest"
    }

db = MySQLdb.connect('localhost', 'root', 'admin','crawler', charset='utf8')
cursor = db.cursor()
errortxt = open('Nosec-error.txt', 'w+', encoding='utf-8')

for i in range(5,10):
    params["page"] = i + 1

    html = session.post(url, data=params, headers=headers)
    html.encoding = html.apparent_encoding
    print(html.status_code)

    with open ("errorhtml.txt",'wb+') as f:
        f.write(html.content)

    res = json.loads(html.text)["data"]["threatData"]["data"]

    sql = "Insert Into Nosec_Threat_Intelligence Values\n"
    for it in res:

        _id = it["id"].replace("'","\\'")
        title = it["title"].replace("'","\\'")
        summary = it["summary"].replace("'","\\'")
        username = it["username"].replace("'","\\'")
        img = it["temp"].replace("'","\\'")

        tmp = "('" + _id + "','" + title + "','" + summary + "','" + username + "','" + img+ "'),\n"
        sql = sql + tmp

    sql = sql[0:len(sql)-2]

    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("Failed to insert db")
        errortxt.write(sql)
        errortxt.close()
        break

    print("第{}页已经爬取到数据库".format(i+1))
    time.sleep(10)
    print("睡眠结束")

errortxt.close()
db.close()
