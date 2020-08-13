import scrapy
from scrapy import Selector
from seebug.items import SeebugItem


class SeebugSpider(scrapy.Spider):
    name = 'seebug_spider'
    allowed_domains = ['www.seebug.org']
    start_urls = ['https://www.seebug.org/vuldb/vulnerabilities']

    def parse(self, response):
        # print(response.text)
        se = Selector(response)
        bug_list = se.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr")
        for i_item in range(len(bug_list)):
            i = i_item+1
            seebug_item = SeebugItem()
            seebug_item['SSV_ID'] = se.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr[%d]/td[1]/a/text()" % i).extract()
            seebug_item['update_time'] = se.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr[%d]/td[2]/text()" % i).extract()


            seebug_item['bug_level'] = se.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr[%d]/td[3]/div" % i).attrib.get('data-original-title')
            seebug_item['bug_name'] = se.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr[%d]/td[4]/a/text()" % i).extract()

            content = se.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr[%d]/td[5]/i/@data-original-title" % i).extract()
            seebug_item['bug_status'] = " ".join(content)
            # print(seebug_item)
            yield seebug_item
        for num in range(2,100):
            yield scrapy.Request("http://www.seebug.org/vuldb/vulnerabilities?page=" + str(num),callback=self.parse)

