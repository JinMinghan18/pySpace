import pymysql
from scrapy.utils.project import get_project_settings

class DBHelper:
    #读取settings中的配置，自行修改代码进行操作

    def __init__(self):
        self.settings = get_project_settings()#获取settings中的配置
        self.host = self.settings['']
