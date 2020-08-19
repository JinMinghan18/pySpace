import scrapy
from newpoc.items import NewpocItem

class NewpocSpiderSpider(scrapy.Spider):
    name = 'newpoc_spider'
    allowed_domains = ['www.seebug.org']
    start_urls = ['http://www.seebug.org/vuldb/vulnerabilities?has_poc=true&page=1']

    def parse(self, response):
        poc_list = response.xpath("/html/body/div[2]/div/div/div/div/table/tbody/tr")
        for i_item in poc_list:
            poc_item = NewpocItem()
            poc_item['ssv_id'] = i_item.xpath("./td[1]/a/text()").extract_first()
            poc_item['name'] = i_item.xpath("./td[4]/a/text()").extract_first()
            poc_item['time'] = i_item.xpath("./td[2]/text()").extract_first()
            poc_item['level'] = i_item.xpath("./td[3]/div/@data-original-title").extract_first()
            content = i_item.xpath("./td[5]/i/@data-original-title").extract()
            content_s = "   ".join(content)
            poc_item['status'] = content_s
            poc_item['evaluate'] = i_item.xpath("./td[6]/text()").extract_first()
            print(poc_item)
            yield poc_item
        for num in range(2, 100):
            yield scrapy.Request("http://www.seebug.org/vuldb/vulnerabilities?has_poc=true&page=" + str(num), callback=self.parse)