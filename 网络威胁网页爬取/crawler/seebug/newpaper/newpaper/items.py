# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewpaperItem(scrapy.Item):

    # 文章名字
    paper_name = scrapy.Field()
    # 发表时间
    paper_time = scrapy.Field()
    # 文章分类
    paper_category = scrapy.Field()
    # 文章介绍
    paper_introduce = scrapy.Field()

