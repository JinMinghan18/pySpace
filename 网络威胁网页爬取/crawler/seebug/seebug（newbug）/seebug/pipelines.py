# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql as db
class SeebugPipeline:
    def __init__(self):
        self.con = db.connect(user="root", passwd="cjk33014423", host="localhost", db="python", charset="utf8")
        self.cur = self.con.cursor()
        self.cur.execute('drop table seebug1')
        self.cur.execute(
            "create table seebug1(ssv_id varchar(255)  primary key,time varchar(40),level varchar(255),name varchar(255),status varchar(255),evaluate varchar(255))")

    def process_item(self, item, spider):
        self.cur.execute(
            "insert into seebug1(ssv_id,time,level,name,status,evaluate) values(%s,%s,%s,%s,%s,%s)",
            (item['ssv_id'], item['time'], item['level'], item['name'], item['status'], item['evaluate']))
        self.con.commit()
        return item
