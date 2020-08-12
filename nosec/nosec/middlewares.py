# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class NosecSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, timeout=None, service_args=None, executable_path=None):
        if service_args is None:
            service_args = []
        self.timeout = timeout
        self.browser = webdriver.PhantomJS(executable_path=executable_path)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()


    def process_request(self, request, spider):
        '''
        用PhantomJs抓取页面
        :param request:
        :param spider:
        :return:
        '''
        self.browser.get(request.url)
        html = self.browser.page_source
        return HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'),executable_path=crawler.settings.get('PHANTOMJS_EXECUTABLE_PATH'))
