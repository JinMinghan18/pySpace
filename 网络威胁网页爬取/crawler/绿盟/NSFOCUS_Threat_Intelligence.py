import requests
from pyquery import PyQuery as pq
import time
import MySQLdb

def getHTML(url):
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
    html = requests.get(url,headers = headers)
    html.encoding = html.apparent_encoding
    return html.text

url = "https://www.nsfocus.com.cn/html/4/348/39/"
       
db = MySQLdb.connect('localhost','root','admin','crawler',charset='utf8')
cursor = db.cursor()
errortxt = open('NSFOCUS-error.txt','w+',encoding='utf-8')

for i in range(8,55):

    if (i == 0):
        tail = "index.html"
    else:
        tail = str(i+1) + ".html"

    html = getHTML(url+tail)

    # with open('3.html','r',encoding='utf-8') as f:
    #     html = f.read()

    doc = pq(html)
    ul = doc('.gong_list').find('ul')
    sql = "Insert Into NSFOCUS_Threat_Intelligence Values\n"

    for li in ul.children('li').items():
        itle = li.find('.itle')
        title = itle.find('p').text()
        date = itle.find('span').text()
        p = itle.next()
        brief = p.text()
        detail_href = p.next().attr('href')
        sql = sql + "('" + title + "','" + date + "','" + brief + "','" + detail_href + "'),\n"

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