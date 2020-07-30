import time
import requests
from bs4 import BeautifulSoup
qy = open('D:/ProgramData/data/weather.txt',mode='a',encoding='utf-8')
res = requests.get('http://www.weather.com.cn/weather15d/101210707.shtml')
res.encoding='utf-8'
html = res.text
soup = BeautifulSoup(html,'html.parser')#解析web 文档

weathers = soup.find(id="15d",class_="c15d").find('ul',class_="t clearfix").find_all('li')
# print(soup)
for weather in weathers:
    weather_date = weather.find('span',class_="time")
    weather_wea = weather.find('span',class_="wea")
    weather_tem = weather.find('span',class_="tem")
    weather_wind = weather.find('span',class_="wind")
    weather_wind1 = weather.find('span',class_="wind1")
    result = '日期' + weather_date.text,'天气:' + weather_wea.text,'温度:' + weather_tem.text, '风向风力：' + weather_wind.text+weather_wind1.text

    print(result)#输出到控制器
    print(result,file=qy)

