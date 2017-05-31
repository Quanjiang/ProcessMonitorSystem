load_info={
  "name":"the name of the script",
  "version":"1.0",
  "email":["a@a.c"],
  "log_file_list":[],
  "ASPScheduler":{
    "type":"interval", #"date","cron"
    "value":{"seconds":12},
  },
  "product":{
    "deploy":"ls",
    "run":"ls -la /",
  },
}


import atexit
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor




jobstores = {
    # 'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url='jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(1)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.start()

from module import task_core

the = task_core.TaskCore(scheduler,None)
the.register('test_1',load_info)

atexit.register(lambda: scheduler.shutdown(wait=False))
import time
while True:
    print('.')
    time.sleep(10)
