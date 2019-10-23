temp_init = '''import os
from flask import Blueprint
from config import BASE_DIR

{} = Blueprint('{}', __name__, 
                template_folder=os.path.join(BASE_DIR,'App/{}/template'),
                static_folder=os.path.join(BASE_DIR,'App/{}/static'))
static_folder = os.path.join(BASE_DIR,'App/{}/static')

from App.{} import views
'''

temp_controllers = '''from App.{} import static_folder
'''

temp_views = '''from App.{} import {}
# @{}.route('/')
# def root():
#    pass
'''

temp_import = '''from .{} import {}
'''

temp_register = '''    app.register_blueprint({}, url_prefix='/{}')
'''
