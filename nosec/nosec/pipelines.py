# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import pymysql.cursors
import codecs
import json
from logging import log

from twisted.enterprise import adbapi


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('info.json','w',encoding='utf-8')#保存为json文件
    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()

class WebcrawlerScrapyPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset='utf-8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False
        )
        dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self._conditional_insert,item)
        query.addErrback(self._handle_error,item,spider)
        return item

    def _conditional_insert(self,tx,item):
        sql = "insert into testtable(name,url) value(%s,%s)"
        params = (item["name"],item["url"])
        tx.execute(sql,params)

    def _handle_error(self,failue,item,spider):
        print('ERROR:database operation exception.数据库操作错误')
        print(failue)