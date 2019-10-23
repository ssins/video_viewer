import os
from flask import Blueprint
from config import BASE_DIR

index = Blueprint('index', __name__, 
                template_folder=os.path.join(BASE_DIR,'App/Index/template'),
                static_folder=os.path.join(BASE_DIR,'App/Index/static'))
static_folder = os.path.join(BASE_DIR,'App/Index/static')

from App.Index import views