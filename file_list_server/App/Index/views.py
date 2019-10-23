from App.Index import index
import os
from config import ROOT_DIR_PATH
from App.Index.controllers import *
import json

@index.route(('/'))
@index.route(('/dir'))
@index.route(('/dir/'))
def root():
    return json.dumps({'path': '/', 'items': getFileAndDirList(ROOT_DIR_PATH)})


@index.route('/dir/<path:dirPath>')
def dir(dirPath=''):
    path = getSubPath(ROOT_DIR_PATH, dirPath)
    if os.path.isdir(path):
        return json.dumps({'path': '/' + getSubPath(dirPath) + '/', 'items': getFileAndDirList(path)})
    else:
        return 'the dir is not exist', 400
