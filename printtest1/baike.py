# coding=UTF-8
import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import PIL.Image as Image
#from apps.web.models import WeatherCityCode
import time
import base64
from io import StringIO



BaiKeConfig = [
    {
        'title': u'行政区划',
        'keywords': [
            u'行政区划'
        ],
        's1':'.section_title',
        'cases':[
            '.next()',
        ],
        'find':'.rich_text_area>div>p',
        'model':'administrative_division'
    },
    {
        'title': u'行政区划',
        'keywords': [
            u'区划详情'
        ],
        's1':'h3',
        'cases':[
            '.next()',
            '.parent().next()',
        ],
        'find':'p',
        'model':'administrative_division1'
    },
    {
        'title': u'人口统计',
        'keywords': [
            u'人口',
        ],
        's1':'.section_title',
        'cases':[
            '.next()',
            '.parent().next()',
        ],
        'find':'.rich_text_area>div:last-child',
        'model':'demographic'
    },
    {
        'title': u'经济',
        'keywords': [
            u'经济',
        ],
        's1':'.section_title',
        'cases':[
            '.parent()',
            '.parent().next()',
            '.parent().parent().next()'
        ],
        'find':'.rich_text_area>div>p:contains("总值")',
        'model':'economic'
    },
    {
        'title': u'交通运输',
        'keywords': [
            u'交通',
        ],
        's1':'.section_title',
        'cases':[
            '.parent()',
            '.parent().parent().next()',
        ],
        'find':'.rich_text_area>div>p',
        'model':'transportation'
    },
    {
        'title': u'交通运输',
        'keywords': [
            u'交通'
        ],
        's1':'h3',
        'cases':[
            '.next()',
            '.parent().next()'
        ],
        'find':'p',
        'model':'transportation1'
    },
    {
        'title': u'地理环境',
        'keywords': [
            u'地理'
        ],
        's1':'.section_title',
        'cases':[
            '.parent()',
            '.parent().parent().next()',
        ],
        'find':'.rich_text_area>div>p',
        'model':'environment'
    },
    {
        'title': u'气候',
        'keywords': [
            u'气候'
        ],
        's1':'h3',
        'cases':[
            '.next()',
            '.parent().next()',
        ],
        'find':'p',
        'model':'weather'
    },
    {
        'title': u'气候',
        'keywords': [
            u'气候'
        ],
        's1':'.section_title',
        'cases':[
            '.parent()',
            '.parent().parent().next()',
        ],
        'find':'.rich_text_area>div>p',
        'model':'weather1'
    },
    {
        'title': u'地形地貌',
        'keywords': [
            u'地形',
            u'地貌'
        ],
        's1':'h3',
        'cases':[
            '.next()',
            '.parent().next()',
        ],
        'find':'p',
        'model':'landform'
    },
    {
        'title': u'水库水系',
        'keywords': [
            u'水',
        ],
        's1':'h3',
        'cases':[
            '.next()',
            '.parent().next()',
        ],
        'find':'p',
        'model':'reservoir'
    },
    {
        'title': u'地震事件',
        'keywords': [
            u'地震事件'
        ],
        's1':'.section_title',
        'cases':[
            '.parent()',
            '.parent().parent().next()',
        ],
        'find':'.rich_text_area>div>p',
        'model':'earthlist'
    }
]


def manager(location):
    # 爬取天气信息
    weatherdriver = webdriver.PhantomJS(executable_path=r"D:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    s = location
    if location.endswith('县') or location.endswith('市'):
        s = location[:-1]
    #codes = WeatherCityCode.objects.filter(name=s)
    codes = "温州"
    weatherData = ''
    if codes:
        weatherdriver.maximize_window()
        weather_url = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(codes[0].code)
        print (weather_url)
        weatherdriver.get(weather_url)
        time.sleep(2)
        try:
            element = WebDriverWait(weatherdriver, 20).until(lambda x: x.find_element_by_id('block-B'))
            left = 183
            top = 284
            right = 183 + element.size['width']
            bottom = 284 + 296
            weatherdriver.save_screenshot('site_media/images/screenshot_temp.png')
            time.sleep(2)
            im = Image.open('site_media/images/screenshot_temp.png')
            im = im.crop((left, top, right, bottom))
            buffer = StringIO.StringIO()
            im.save(buffer, format="PNG")
            weatherData = base64.b64encode(buffer.getvalue())

        finally:
            weatherdriver.quit()

    req1 = requests.get(
        'https://baike.sogou.com/enterBarLemma.v?searchText=%s' % (location))
    reql_url = req1.text
    print (reql_url)
    driver = webdriver.PhantomJS()
    print('---模拟动态网页开始---')
    time.sleep(5)
    driver.get('https://baike.sogou.com%s' % reql_url)
    time.sleep(10)
    data = driver.page_source
    driver.quit()

    result = {}
    if len(weatherData) > 0:
        result['weatherData'] = weatherData
    print('---模拟动态网页结束---')
    content = pq(data)
    for item in BaiKeConfig:
        exist = False
        sections = content.find(item['s1'])
        for sec in sections:
            source = pq(sec)
            for keyword in item['keywords']:
                if keyword in source.text():
                    for case in item['cases']:
                        data = eval('pq(sec)' + case).find(item['find']).text()
                        if data:
                            exist = True
                            result[item['model']] = data
                            break
                    break
            if exist:
                break

    print('爬取结束')
    return result

if __name__ == '__main__':
    result = manager('唐山')
    for k, v in result.items():
        print ("=======%s=========" % k)
        print (v)
