import requests
import re
from pyquery import PyQuery as pq
import time
import pymysql
import pymysql
import json
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
url = 'https://portal.msrc.microsoft.com/api/security-guidance/zh-cn'

# jobstores = {
#     'default':SQLAlchemyJobStore(url='mysql+pymysql://root:123456@127.0.0.1/apscheduler?charset=utf-8',tablename='microsoft')
# }

def get_HTML(url,from_data):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
              'Content-Type':'application/json; charset=utf-8'}
    cookies = {'Cookies':'your cookie'}
    html = requests.post(url,data=from_data,headers=headers,cookies=cookies)
    html.encoding = html.apparent_encoding
    return html.text
data = {
    "familyIds": [],
    "filterText": "",
    "fromPublishedDate": "06/10/2020",
    "impactIds": [],
    "includeCveNumber": True,
    "includeImpact": True,
    "includeSeverity": True,
    "isDescending": True,
    "isDescendingMonthly": True,
    "isSearch": False,
    "orderBy": "publishedDate",
    "orderByMonthly": "releaseDate",
    "pageNumber": 2,
    "pageSize": 100,
    "productIds": [],
    "queryText": "",
    "severityIds": [],
    "toPublishedDate": "08/01/2020"
}

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",password="123456",
    database="apsecheduler",
    charset="utf8"
)

cursor = conn.cursor()

for i in range(27,35):
    data["pageNumber"] = i + 1
    html = get_HTML(url,json.dumps(data))
    #get data from details
    result = json.loads(html)["details"]
    #execute database
    sql = "Insert into microsoft Values"
    for it in result:
        tmp = "("
        for littleit in it:
            if type(it[littleit]) is str:
                tmp = tmp + "'" + it[littleit] + "',"
            elif type(it[littleit]) is int:
                tmp = tmp + str(it[littleit]) + ","
            elif type(it[littleit]) is bool:
                tmp = tmp + str(it[littleit]) + ","
            elif it[littleit] is None:
                tmp = tmp + "null,"
        tmp = tmp[0:len(tmp)-1]+"),\n"
        # print(tmp)
        sql += tmp
    sql = sql[0:len(sql)-2]
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        print("failed")
    print("number{} is already".format(i+1))
    time.sleep(1)
    print("restart")
conn.close()