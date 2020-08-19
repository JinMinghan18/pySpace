import scrapy
from seebug.items import SeebugItem

class SeebugSpiderSpider(scrapy.Spider):
    name = 'seebug_spider'
    allowed_domains = ['www.seebug.org']
    start_urls = ['http://www.seebug.org/vuldb/vulnerabilities?page=1']

    def parse(self, response):
        bug_list=response.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr")
        for i_item in bug_list:
            seebug_item=SeebugItem()
            seebug_item['ssv_id']=i_item.xpath("./td[1]/a/text()").extract_first()
            seebug_item['name'] = i_item.xpath("./td[4]/a/text()").extract_first()
            seebug_item['time'] = i_item.xpath("./td[2]/text()").extract_first()
            seebug_item['level'] = i_item.xpath("./td[3]/div/@data-original-title").extract_first()
            content=i_item.xpath("./td[5]/i/@data-original-title").extract()
            content_s="   ".join(content)
            seebug_item['status'] =content_s
            seebug_item['evaluate'] = i_item.xpath("./td[6]/text()").extract_first()
            yield seebug_item
        for num in range(2, 101):
            yield scrapy.Request("http://www.seebug.org/vuldb/vulnerabilities?page=" + str(num),callback=self.parse)
        #last = response.xpath("/html/body/div[2]/div/div/nav/ul/li[last()-1]/a/text()").extract()
        #str_last="".join(last)
        #int_last=int(str_last)
        #for i in range(2,int_last):
            #yield scrapy.Request("http://www.seebug.org/vuldb/vulnerabilities?page=" + str(i), callback=self.parse)
