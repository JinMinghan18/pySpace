# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeebugItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SSV_ID = scrapy.Field()
    update_time = scrapy.Field()
    bug_level = scrapy.Field()
    bug_name = scrapy.Field()
    bug_status = scrapy.Field()