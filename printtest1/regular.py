from apscheduler import job
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging
import spider

# 日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')



# 任务
def my_job(id, num):
    pass
    # print(num, id, '-->', datetime.datetime.now())


# 报错任务
def error_job(id):
    # print(id, '-->', datetime.datetime.now())
    print(1 / 0)


# 监听事件
def my_listener(event):
    if event.exception:
        print("jobs error")
    else:
        print("normal")


# 配置调度器
jobstores = {
    'default': SQLAlchemyJobStore(url='mysql+pymysql://root:Ji1234@101.132.131.184/apscheduler?charset'
                                      '=utf8', tablename='api_job')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

if __name__ == "__main__":
    scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    # 添加监听器
    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # 日志打印
    scheduler._logger = logging

    scheduler.add_job(func=spider.update, id='spider', trigger='interval', seconds=3,
                      replace_existing=True)
    # 启动调度器
    scheduler.start()
