# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from douban.settings import database_host,database_port,database_name,database_collection

class DoubanPipeline:
    def __init__(self):
        self.mydb = pymysql.connect(host = database_host,user = "root",password="123456",database="douban",charset="utf8",use_unicode=True)
        self.cursor = self.mydb.cursor()
    def process_item(self, item, spider):
        insert_sql = "insert into douban_movie_top250(serial_number,movie_name,introduce,star,evaluate,describetion)values(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(insert_sql,(item['serial_number'],item['movie_name'],item['introduce'],item['star'],item['evaluate'],item['describetion']))
        self.mydb.commit()
    def close_spider(self,spider):
        self.cursor.close()
        self.mydb.close()