# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from seebug.settings import *


class SeebugPipeline:
    def __init__(self):

        self.mydb = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWD, database=MYSQL_DBNAME,
                                    port=MYSQL_PORT, charset='utf8', use_unicode=True)
        self.cursor = self.mydb.cursor()

    def process_item(self, item, spider):
        insert_sql = "insert into buginfo(SSV_ID,update_time,bug_level,bug_name,bug_status)values(%s,%s,%s,%s,%s)"

        self.cursor.execute(insert_sql, (item['SSV_ID'], item['update_time'], item['bug_level'], item['bug_name'], item['bug_status']))
        self.mydb.commit()

    def close_spider(self, spider):

        self.cursor.close()
        self.mydb.close()
