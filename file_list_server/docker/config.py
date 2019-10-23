import os
BASE_DIR = os.getcwd()
PRODUCT_NAME = 'simple'
ENV = 'debug'
# ENV = 'docker'

# flask server
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 3333
FLASK_DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1qaz2wsx@localhost:3306/' + PRODUCT_NAME
if ENV == 'docker':
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1qaz2wsx@172.17.0.2:3306/'  + PRODUCT_NAME
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# root user name
# change the database value if you changed this value
ROOT_NAME = 'root'

# root dir path
ROOT_DIR_PATH = './files/'