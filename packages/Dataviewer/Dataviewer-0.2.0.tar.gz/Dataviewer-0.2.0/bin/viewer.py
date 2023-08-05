import json
import logging
import os
import random
import shlex
import string
import subprocess
from datetime import datetime
from functools import update_wrapper, wraps

from flask import (Flask, Response, jsonify, make_response, request, send_file,
                   send_from_directory)
import pkg_resources

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)
    
tasks = {}
app = Flask(__name__)
dist = pkg_resources.resource_filename('dataviewer', 'dist')

if "PRODUCTION" not in os.environ:
    from flask_cors import CORS
    CORS(app)

@app.route('/<path:path>')
@nocache
def assets(path="index.html"):
    return send_from_directory(dist, path)

@app.route("/")
@nocache
def index():
    return send_from_directory(dist, 'index.html')

def setupApp(folder, host, port):
    print " * IMDC, nv "
    print " * Contact: kdd@imdc.be"
    print " * Starting dataviewer for folder %s " % folder
    print " * running on http://%s:%s"%(host, port)

    @app.route('/tree')
    @nocache
    def send_tree():
        dir = {}
        rootdir = folder
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir
        return jsonify(dir[os.path.basename(rootdir)])

    @app.route('/data/<path:path>')
    @nocache
    def send_data(path):
        return send_from_directory(folder, path)

    return app

if __name__ == "__main__":
    import sys
    args = sys.argv
    from optparse import OptionParser
    parser = OptionParser(usage="Start the python server for the dataviewer tool.")
    parser.add_option("-p", "--port", dest="port", help="Port for the server to run on. Default = 80", default=80, type="int")
    parser.add_option('-H', '--host', dest='host', help='Host for the server to run on. Default = localhost', default='localhost')    
    (options, args) = parser.parse_args(args)
    
    app = setupApp(folder=args[1], host=options.host, port=options.port)
    app.run(threaded=True, port=options.port, host=options.host)
