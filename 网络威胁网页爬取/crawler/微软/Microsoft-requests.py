import requests
from pyquery import PyQuery as pq
import time
import MySQLdb
import json

def getHTML(url,form_data):
    # 设置content-type和user-agent
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                'Content-Type':'application/json; charset=utf-8'}
    cookies = {'Cookies':'your cookie'}
    html = requests.post(url,data=form_data,headers=headers,cookies = cookies)
    html.encoding = html.apparent_encoding
    return html.text

# 提交的表单数据
data = {"familyIds": [],
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
"pageNumber": 1,
"pageSize": 100,
"productIds": [],
"queryText": "",
"severityIds": [],
"toPublishedDate": "07/28/2020",}

url = "https://portal.msrc.microsoft.com/api/security-guidance/zh-cn"

# 连接数据库
db = MySQLdb.connect('localhost','root','123456','crawler', charset='utf8')
cursor = db.cursor()

# 每页100条，一共34页
for i in range(0,34):
    # 更改表单的页数
    data["pageNumber"] = i + 1
    # 得到json格式的字符串
    html = getHTML(url,json.dumps(data))
    # f = open('tmp.txt','w',encoding='utf-8')
    # f.write(html)

    # f = open('tmp.txt','r',encoding='utf-8')
    # html = f.read()
    # f.close()

    # 从json格式中获取details对应的数据
    res = json.loads(html)["details"]
    # 生成对应的sql语句
    sql = "Insert Into Microsoft Values"
    for it in res:
        tmp = "("
        for it2 in it:
            if type(it[it2]) is str:
                tmp = tmp + "'" + it[it2] + "',"
            elif type(it[it2]) is int:
                tmp = tmp + str(it[it2]) + ","
            elif it[it2] is None:
                tmp = tmp + "null,"
            elif type(it[it2]) is bool:
                tmp = tmp + str(it[it2]) + ","
        # 去除末尾逗号
        tmp = tmp[0:len(tmp)-1] + "),\n"
        # print(tmp)
        sql = sql + tmp

    # 去除末尾换行符和逗号
    sql = sql[0:len(sql)-2]
    # print(sql)

    # 添加到数据库
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("Failed to insert db")

    print("第{}页已经爬取到数据库".format(i+1))
    time.sleep(60)
    print("睡眠结束")

db.close()