# -*- coding: utf-8

from flask import Blueprint, jsonify
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

import builtin
from error import BadRequest, Unauthorized, PermissionDenied, NotFound, Conflict
from model import Music, Star, Tag, User, login_manager
from form import RegisterForm, LoginForm


bp = Blueprint('api', __name__)

# User

@bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate():
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        email = form.email.data

        if password != password2:
            return jsonify(code=200, msg='两次输入的密码不一致')

        udoc = User.objects(username=username).first()
        if udoc:
            return jsonify(code=201, msg='用户名已存在')

        udoc = User.objects(email=email).first()
        if udoc:
            return jsonify(code=201, msg='邮箱已存在')

        udoc = User(username=username, passwordHash=generate_password_hash(password),
                    email=email, role=builtin.ROLE_DEFAULT)
        udoc.save()

        return jsonify(code=0, data=udoc)

    else:
        return jsonify(code=200, msg=next(iter(form.errors.values()))[0])

@bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate():
        username = form.username.data
        password = form.password.data
        udoc = User.objects(username=username).first()
        if not udoc:
            raise Unauthorized('用户名或密码错误')
        if not check_password_hash(udoc.passwordHash, password):
            raise Unauthorized('用户名或密码错误')
        login_user(udoc)

        return jsonify(udoc)
    else:
        raise BadRequest(next(iter(form.errors.values()))[0])

@bp.route('/logout')
def logout():
    logout_user()
    return jsonify(code=0)

@bp.route('/users')
@login_required
def get_users():
    udocs = User.objects()
    return jsonify(code=0, data=udocs)

@bp.route('/users/<string:username>')
@login_required
def get_user(username):
    udoc = User.objects(username=username)
    if udoc:
        return jsonify(code=0, data=udoc)
    else:
        return jsonify(code=201, msg='用户不存在')

@bp.route('/users/<string:uid>', methods=['PUT'])
@login_required
def update_user(uid):
    return 'put' + uid

# Music
@bp.route('/music')
def get_multiple_music():
    pass

@bp.route('/music', methods=['POST'])
@login_required
def create_music():
    pass

@bp.route('/music/<string:mid>')
def get_music(mid):
    pass

@bp.route('/music/<string:mid>', methods=['PUT'])
@login_required
def update_music(mid):
    pass

# Search

@bp.route('/search')
def ajax_search():
    pass

@bp.route('/search', methods=['POST'])
def search():
    pass
