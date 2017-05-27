#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#
import os
import os.path as osp


virtenv = osp.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'venv')
virtualenv =osp.join(virtenv,'bin/activate_this.py')
try:
    exec(open(virtualenv).read(), dict(__file__=virtualenv))
except IOError:
    pass

from main import app as application

if 'OPENSHIFT_APP_NAME' in os.environ:              #are we on OPENSHIFT?
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
else:
    ip = '0.0.0.0'                            #localhost
    port = 8051


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    print("Serving at http://localhost:8051/ \n PRESS CTRL+C to Terminate. \n")
    httpd.serve_forever()
    print("Terminated!!")
#
# Below for testing only
#
