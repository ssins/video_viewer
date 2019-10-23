from flask import Flask, request, g
from flask_httpauth import HTTPTokenAuth
from App.models import *
from config import ROOT_NAME
from functools import wraps

auth = HTTPTokenAuth(scheme='Bearer')

# 登录验证装饰器
@auth.verify_token
def verify_token(token):
    if token:
        g.user = User.query.filter_by(token=token).first()
        if g.user:
            return True
    return False

# 管理员操作权限装饰器
def root_requied(fn):
    @wraps(fn)
    def verify_root(*args):
        if g.user and g.user.user_name == ROOT_NAME:
            return fn(*args)
        return 'Permission denied', 500
    return verify_root
