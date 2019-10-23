from App.User import user
from App.User.controllers import *
from flask import Flask, request, g
from App.decorators import auth, root_requied
from config import ROOT_NAME


@user.route('/regist', methods=['Post'])
def regist():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    if user_name and password:
        return regist_user(user_name, password)
    return 'args error', 400


@user.route('/login', methods=['Post'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    if user_name and password:
        return login_user(user_name, password)
    return 'args error', 400


@user.route('/reset', methods=['Post'])
@auth.login_required
def reset():
    user_name = request.form.get('user_name')
    if user_name:
        password = request.form.get('password')
        if password:
            return reset_pwd_root(user_name, password)
        return 'args error', 400
    old = request.form.get('old')
    password = request.form.get('password')
    if old and password:
        return reset_pwd(old, password)
    return 'args error', 400


@user.route('/delete', methods=['Post'])
@auth.login_required
@root_requied
def delete():
    user_name = request.form.get('user_name')
    if user_name:
        if user_name != ROOT_NAME:
            return delete_user(user_name)
        return 'can not delete root', 500
    return 'args error', 400

@user.route('/list', methods=['Post', 'Get'])
@auth.login_required
@root_requied
def getlist():
    return list_user()
