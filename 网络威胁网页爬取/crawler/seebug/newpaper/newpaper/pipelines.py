# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql as db

class NewpaperPipeline:
    def __init__(self):
        self.con = db.connect(user="root", passwd="jin123456", host="39.97.238.64", db="seebug", charset="utf8")
        self.cur = self.con.cursor()
        # self.cur.execute('drop table seebug2')
        # self.cur.execute(
        #     "create table seebug2(paper_name varchar(255),paper_time varchar(40),paper_category varchar(255),paper_introduce varchar(255))")

    def process_item(self, item, spider):
        self.cur.execute(
            "insert into newpaper(paper_name,paper_time,paper_category,paper_introduce) values(%s,%s,%s,%s)",
            (item['paper_name'], item['paper_time'], item['paper_category'], item['paper_introduce']))
        self.con.commit()
        return item
