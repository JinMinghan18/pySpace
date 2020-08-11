import scrapy
from scrapy import Selector

from nosec.items import NosecItem

class NosecThreatSpiderSpider(scrapy.Spider):
    name = 'nosec_threat_spider'
    allowed_domains = ['https://nosec.org/'] #在此域名范围内搜素哦
    start_urls = ['https://nosec.org/home/index/security.html']#开始搜索的域名

    def parse(self, response):
        se = Selector(response)
        asrc = se.xpath("//div[@id='article-content']")
        for i_item in range(len(asrc)):
            aurl = i_item.xpath(".//div[%d]/div[2]/a" % i_item).attrib.get("href")
            filename = i_item.xpath(".//div[%d]/div[2]/a/text()" % i_item).extract()
            item = NosecItem()
            item['name'] = filename
            item['url'] = aurl
            print("*****NAME*****")
            print(filename)
            print("*****NAME******")
            print("*****URL******")
            print(aurl)
            print("*****URL******")
            yield item
