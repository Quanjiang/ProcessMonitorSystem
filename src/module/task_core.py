#
# This module contain all function relate the mulit-process monitor by

import os
import time
import os.path as osp
import subprocess

from src.module import db

class TaskCore:


    def __init__(self,scheduler,log,taskpath="./task"):
        self.scheduler = scheduler
        self.log = log
        self.db = db.DBConnect()
        self.task_path =taskpath

    def _job_entry(name_id,task_path,load_info):
        #
        #
        self.db.set_status(name_id,'start')
        self.log.info('[STR] {} - {}'.format(name_id,task_path))
        def _writeintofile(stdout,stderr,path,name_id):
            with open(osp.join(path,"{}.stdout".format(name_id)),'w') as wh:
                wh.write(stdout.decode('utf8'))
            with open(osp.join(path,"{}.stderr".format(name_id)),'w') as wh:
                wh.write(stderr.decode('utf8'))
        #
        fpath= osp.join(task_path,name_id)
        srcpath = osp.join(fpath,'src')
        confpath = osp.join(fpath,'.pms')
        logpath = osp.join(fpath,'log',str(time.time()))

        #bad code style here
        if not osp.exists(logpath):
            os.system('mkdir -p '+logpath)
        if not osp.exists(confpath):
            os.system('mkdir -p ' + confpath)

        if not osp.exists(osp.join(confpath,'deployed')):
            self.db.set_status(name_id,'deployed')
            rtn = subprocess.Popen([load_info['product']['deploy']],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout,stderr = rtn.communicate()
            _writeintofile(stdout,stderr,logpath,'deployed')
            os.system('touch '+osp.join(confpath,'deployed'))

        #TODO: here should make it support Websocket
        self.db.set_status(name_id,'runing')
        rtn = subprocess.Popen([load_info['product']['run']],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        stdout,stderr = rtn.communicate()
        _writeintofile(stdout,stderr,logpath,'run')
        self.db.set_status(name_id,'done')

        #here was the log deal process
        self.db.set_status(name_id,'backup log')
        for each_log in load_info['log_file_list']:
            temp = osp.join(fpath,'src',each_log)
            if osp.exists(temp):
                os.system('cp -f {} {}/'.format(temp,logpath))
        self.db.set_status(name_id,'Not Running')

    def register(self,name_id,load_info):
        #
        rtn = self.scheduler.add_job(TaskCore._job_entry, trigger=load_info['ASPScheduler']['type'], args=None, kwargs={'name_id':name_id,'task_path':self.task_path,'load_info':load_info}, id=name_id, name=name_id, \
                    misfire_grace_time=2, coalesce=5, max_instances=10, \
                    jobstore='default', executor='processpool', replace_existing=True, **load_info['ASPScheduler']['value'])
        self.log.info(rtn)

    def queryStatus(self,name_id):
        #
        tjob = self.scheduler.get_job(name_id)
        return self.db.get_status(name_id),tjob.next_run_time


    # def deregister(self,name_id):
    #     #Deregister the task
    #     self.scheduler.remove_job(self.dbop.getIDbyname_id(name_id))
    #
    # def pause(self,name_id):
    #     #
    #     self.scheduler.pause_job(self.dbop.getIDbyname_id(name_id))
    #
    # def resume(self,name_id):
    #     #
    #     self.scheduler.resume_job(self.dbop.getIDbyname_id(name_id))
