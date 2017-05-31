from flask import Flask,render_template,request
from flask_socketio import SocketIO
import atexit
import logging
import logging.handlers
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from src.module import task_core
import json

TASK_PATH='./task'

jobstores = {
    # 'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url='jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
def get_logger(logfilename):
    """! get the logging instance
    @return return the instance of logging
    """
    # logfilename = '/dfcxact/dogfish.log'
    logger = logging.getLogger('PMS')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s  %(levelname)s %(message)s')
    fh = logging.handlers.TimedRotatingFileHandler(logfilename, 'W0', 1, 0)
    fh.suffix = "%Y%m%d-%H%M.log"
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    consol =  logging.StreamHandler()
    consol.setFormatter(formatter)
    logger.addHandler(consol)
    return logger

logobj = get_logger('pms.log')

logobj.info('Starting scheduler...')
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=True))

logobj.info('Starting TaskCore...')
taskobj = task_core.TaskCore(scheduler,logobj,TASK_PATH)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# socketio.run(app)

@app.route('/')
def index():
    # return 'hello workd'
    return render_template('index.html')
@app.route('/add')
def add():
    return render_template('add.html')
@app.route('/query')
def query():
    name_id = request.args.get('name_id',None)
    return render_template('query.html')


@app.route('/get_all')
def get_all():
    try:
        rtn =  taskobj.db.get_all_list()
    except Exception as e:
        return json.dumps({'err':8,'msg':'unknow failed happen!:{}'.format(e)})
    return json.dumps({'err':0,'list':rtn})



def get_job(name_id):

    if name_id == None:
        return "{'err':6,'msg':'incorrect name_id'}"

    try:
        status,path =  taskobj.db.get_record(name_id)
    except:
        return "{'err':7,'msg':'unknow name id'}"

    with open(path,'r') as rh:
        try:
            exec(rh.readliens(),globals(),locals())
        except:
            return "{'err':4,'msg':'unknow pms.json:{}'}".format(tpath)
        load_info = locals()['load_info']
        return json.dumps({'err':0,'load_info':load_info,'status':status,'path':path}) #need transfer to json foramt


@app.route('/add_job')
def add_job():
    git_address = request.form.get('git_address',None)
    name_id = request.form.get('name_id',None)
    ispull_lastcode_before_run = request.form.get('pull_lastcode_before_run',False)

    if git_address== None or name_id == None:
        return "{'err':1,'msg':'Incorrect input'}"

    # git clone the address
    if not taskobj.db.check_name_id(name_id):
        return  "{'err':2,'msg':'repeate name_id'}"

    tpath =osp.join(TASK_PATH,name_id)
    if osp.exists(tpath):
        return  "{'err':3,'msg':'folder existed on path:{}'}".format(tpath)
    else:
        os.system('mkdir -p '+tpath)
        #TODO here should monitor the git process.
        os.system('git clone {} {}/src'.format(git_address,tpath))
        time.sleep(5)

    #load the load_info section
    with open(osp.join(tpath,'src','pms.json'),'r') as rh:
        try:
            exec(rh.readliens(),globals(),locals())
        except:
            return "{'err':4,'msg':'unknow pms.json:{}'}".format(tpath)
        load_info = locals()['load_info']

        try:
            taskobj.db.register_record(name_id,osp.join(tpath,'src','pms.json'))
            taskobj.register(name_id,load_info)
        except Exception as e:
            taskobj.db.set_status(name_id,'failed')
            return "{'err':5,'msg':can not start'{}',{}}".format(tpath,e)
    return "{'err':0,'msg':''}"
