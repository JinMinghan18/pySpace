# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeebugItem(scrapy.Item):

    #ssv_id
    ssv_id=scrapy.Field()
    #提交时间
    time=scrapy.Field()
    #漏洞等级
    level=scrapy.Field()
    #漏洞名称
    name=scrapy.Field()
    #漏洞状态
    status=scrapy.Field()
    #人气|评论
    evaluate=scrapy.Field()