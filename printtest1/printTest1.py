# import datetime
# from apscheduler.schedulers.blocking import BlockingScheduler
# def printtest1():
#     print(datetime.datetime.now())
# scheduler = BlockingScheduler()
# scheduler.add_job(printtest1,'interval',seconds=5, id='printtest1')
# scheduler.start()


# from datetime import *
# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler()
# def printtest1(text):
#     print(text)
# scheduler.add_job(printtest1,'date',run_date = datetime(2020,7,24,21,57,00), args=['测试'])
# scheduler.start()

import time
import datetime
from apscheduler.schedulers.background import BlockingScheduler,BackgroundScheduler
def printtest1(text):
    print( "test1" , text)
schedulers = BackgroundScheduler()
schedulers.add_job(func=printtest1,id='printtest1',trigger='cron',second='*/5',args=[datetime.datetime.now()])
schedulers.start()
while(True):
    print('1s')
    time.sleep(1)
