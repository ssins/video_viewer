import os
from flask import Blueprint
from config import BASE_DIR

user = Blueprint('user', __name__, 
                template_folder=os.path.join(BASE_DIR,'App/User/template'),
                static_folder=os.path.join(BASE_DIR,'App/User/static'))
static_folder = os.path.join(BASE_DIR,'App/User/static')

from App.User import views
