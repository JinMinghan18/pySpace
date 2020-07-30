import urllib.request
import ssl
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
from io import StringIO
import base64
class Code:
    def __init__(self,city,code):
        self.city=city
        self.code=code
codes=[]
codes.append(Code("武汉","101200101"))
codes.append(Code("杭州","101210101"))
weatherdriver = webdriver.PhantomJS(executable_path=r"D:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe")

if codes:
    weatherdriver.maximize_window()
    weather_url = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(codes[0].code)
    #weather_url = 'https://www.iqiyi.com/home2020'
    print(weather_url)
    weatherdriver.get(weather_url)
    time.sleep(2)
    print(1)
    try:
        print(3)
        element = WebDriverWait(weatherdriver,5).until(lambda x:x.find_element_by_id('today'))
        print(2)
        a1 = 315
        b1 = 204
        a2 = 608
        b2 = 853
        weatherdriver.save_screenshot('sc.png')
        time.sleep(2)
        im = Image.open('sc.png')
        im = im.crop((b1,a1,b2,a2))
        im.save("buffer.png",format="PNG")
    finally:
        print("end")
        #weatherdriver.quit()
