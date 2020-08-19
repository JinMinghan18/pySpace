import requests
from pyquery import PyQuery as pq
import time
import MySQLdb

def getHTML(url):
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    html = requests.get(url,headers = headers)
    html.encoding = html.apparent_encoding
    return html.text

# url = "https://ti.qianxin.com/advisory/"
url = "https://ti.qianxin.com/advisory/pages/3/"

db = MySQLdb.connect('localhost','root','admin','crawler',charset='utf8')
cursor = db.cursor()
errortxt = open('QiAnXin-error.txt','w+',encoding='utf-8')

html = getHTML(url)

doc = pq(html)
art_list = doc('.art-list')
sql = "Insert Into QiAnXin_Threat_Intelligence Values\n"

for art_container in art_list.children().items():
    text_box = art_container('.text-box')
    title = text_box('.title-home').text()
    author = text_box('.author').text()
    brief = text_box('.brief').text()
    tags = art_container('span')

    tmp = "('" + title + "','" + author + "','" + brief + "','" + tags.text() + "'),\n"
    sql = sql + tmp

sql = sql[0:len(sql) - 2]

try:
    cursor.execute(sql)
    db.commit()
except:
    print("Failed to insert db")
    errortxt.write(sql)

errortxt.close()
db.close()