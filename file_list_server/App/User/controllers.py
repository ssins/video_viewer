from App.User import static_folder
from App.models import db, User
from App.cryptor import PrpCrypt
import json
import random
import string
from App.decorators import root_requied
from flask import g
from App.models import AlchemyJsonEncoder


def regist_user(user_name, password):
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        return 'user_name exist', 401
    user = User(user_name, password)
    db.session.add(user)
    db.session.commit()
    return 'success'


def login_user(user_name, password):
    user = User.query.filter_by(user_name=user_name, password=password).first()
    if user:
        key = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        user.key = key
        js = json.dumps([{'user_name': user_name, 'password': password}])
        crypt = PrpCrypt(key)
        token = crypt.encrypt(js).decode(encoding='utf-8')
        user.token = token
        db.session.add(user)
        db.session.commit()
        return json.dumps({"token": token})
    return 'user_name or password error', 401


@root_requied
def reset_pwd_root(user_name, password):
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        user.password = password
        user.key = ''
        user.token = ''
        db.session.add(user)
        db.session.commit()
        return 'success'
    return 'user not exist', 401


def reset_pwd(old, password):
    if g.user and g.user.password == old:
        g.user.password = password
        g.user.key = ''
        g.user.token = ''
        db.session.add(g.user)
        db.session.commit()
        return 'success'
    return 'old password error', 500


def delete_user(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        for per in user.permissions:
            db.session.delete(per)
        db.session.delete(user)
        db.session.commit()
        return 'success'
    return 'user_name error', 401


def list_user():
    users = User.query.all()
    return json.dumps(users, cls=AlchemyJsonEncoder)
