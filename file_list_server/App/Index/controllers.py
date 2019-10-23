from App.Index import static_folder
import re
import os


def getSubPath(*pathStr):
    rst = []
    for pStr in pathStr:
        l = re.split(r'[/\\]', pStr)
        while '' in l:
            l.remove('')
        rst.extend(l)
    return '/'.join(rst)


def getFileAndDirList(path):
    rst = []
    files = os.listdir(path)
    for f in files:
        if os.path.isdir(getSubPath(path, f)):
            rst.append({'type': 'dir', 'name': f})
        elif os.path.isfile(getSubPath(path, f)):
            rst.append({'type': 'file', 'name': f})
    return rst
