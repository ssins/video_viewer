from flask import Flask
from config import MAX_CONTENT_LENGTH, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from .models import db
from .Index import index
from .User import user
# >>import<< 代码自动生成标签，请勿删除或编辑本行


def create_app():
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(index, url_prefix='/index')
    app.register_blueprint(user, url_prefix='/user')
    # >>register<< 代码自动生成标签，请勿删除或编辑本行
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    return app, db
