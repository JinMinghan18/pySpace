import scrapy
from newpaper.items import NewpaperItem

class NewpaperSpiderSpider(scrapy.Spider):
    name = 'newpaper_spider'
    allowed_domains = ['paper.seebug.org']
    start_urls = ['http://paper.seebug.org/']

    def parse(self, response):
        paper_list = response.xpath("//*[@id='wrapper']/main/div/article")
        for i_item in paper_list:
            newpaper_item = NewpaperItem()
            newpaper_item['paper_name']=i_item.xpath("./header/h5/a/text()").extract_first()
            newpaper_item['paper_time'] = i_item.xpath("./header/section/span/time[2]/text()").extract_first()
            content = i_item.xpath("./header/section/a/text()").extract()
            content_s = "".join(content)
            newpaper_item['paper_category'] =content_s
            newpaper_item['paper_introduce'] = i_item.xpath("normalize-space(./section/text())").extract_first()
            print(newpaper_item)
            yield newpaper_item
        for num in range(2, 101):
            yield scrapy.Request("https://paper.seebug.org/?page=" + str(num),callback=self.parse)
            #next_link=response.xpath("//*[@id='wrapper']/main/div/nav/a/@href").extract()