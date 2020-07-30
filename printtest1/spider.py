from selenium.webdriver.edge.service import Service
from selenium import webdriver


def update():
    print("spider update")
    service = Service('D:\ProgramData\Anaconda3\Scripts\msedgedriver.exe')
    service.start()
    driver = webdriver.Remote(service.service_url)
    driver.get('http://weather.sina.com.cn')
    data = driver.find_elements_by_class_name('slider_degree')[0]
    print(data.text)
    driver.quit()
