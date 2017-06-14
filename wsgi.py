#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
import os
import os.path as osp
from flask_socketio import SocketIO

virtenv = os.environ.get('OPENSHIFT_PYTHON_DIR', '.') + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    # See: http://stackoverflow.com/questions/23418735/using-python-3-3-in-\
    # openshifts-book-example?noredirect=1#comment35908657_23418735
    # execfile(virtualenv, dict(__file__=virtualenv)) # for Python v2.7
    # exec(compile(open(virtualenv, 'rb').read(), virtualenv, 'exec'),
    #  dict(__file__=virtualenv)) # for Python v3.3
    # Multi-Line for Python v3.3:
    exec_namespace = dict(__file__=virtualenv)
    with open(virtualenv, 'rb') as exec_file:
        file_contents = exec_file.read()
    compiled_code = compile(file_contents, virtualenv, 'exec')
    exec(compiled_code, exec_namespace)
except IOError:
    pass

# from src.routes import  app, socketio
import src.routes

if 'OPENSHIFT_APP_NAME' in os.environ:              # are we on OPENSHIFT?
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
else:
    ip = '0.0.0.0'                            # localhost
    port = 8051


if __name__ == '__main__':
    # socketio = SocketIO(application)
    # socketio.run(application, debug=True)
    src.routes.start()

    # from wsgiref.simple_server import make_server
    # httpd = make_server('localhost', 8051, app)
    # print("Serving at http://localhost:8051/ \n PRESS CTRL+C to Terminate. \n")
    # httpd.serve_forever()
    # print("Terminated!!")
#
# Below for testing only
#