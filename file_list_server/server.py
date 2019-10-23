from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, ROOT_NAME
from flask import redirect, url_for
from App import create_app
from App.models import *
import gunicorn
import gevent

app, db = create_app()


@app.route('/')
def root():
    return redirect(url_for('index.root'))

# 初始化数据库
@app.route('/init')
def init():
    try:
        db.drop_all()
        db.create_all()
        # 初始化root用户
        root = User(ROOT_NAME, ROOT_NAME)
        db.session.add(root)
        db.session.commit()
    except:
        return 'fail'
    return 'success'

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
