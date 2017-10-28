# -*- coding: utf-8

from functools import wraps
from bson.objectid import ObjectId

from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from schema import SchemaError

import builtin
from error import APIException, BadRequest, Unauthorized, PermissionDenied, NotFound, Conflict
from model import Music, Star, Tag, User, login_manager
from validator import RegisterSchema, LoginSchema, CreateMusicSchema, QueryMusicParam

bp = Blueprint('api', __name__)

@bp.errorhandler(APIException)
def api_error(error):
    resp = jsonify(message = error.message)
    resp.status_code = error.status_code
    return resp

@bp.before_request
def check_json():
    if request.method != 'GET' and not request.is_json:
        raise BadRequest('不是合法的json请求')

def validate(validator):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                data = validator.validate(request.json)
            except SchemaError as e:
                raise BadRequest(str(e))
            return func(data, *args, **kwargs)
        return wrapper
    return decorator

# User
@bp.route('/register', methods=['POST'])
@validate(RegisterSchema)
def register(data):
    username = data['username']
    password = data['password']
    password2 = data['password2']
    email = data['email']

    if password != password2:
        raise BadRequest('两次输入的密码不一致')

    udoc = User.objects(username=username).first()
    if udoc:
        raise Conflict('用户名已存在')

    udoc = User.objects(email=email).first()
    if udoc:
        raise Conflict('邮箱已存在')

    udoc = User(username=username, passwordHash=generate_password_hash(password),
                email=email, role=builtin.ROLE_DEFAULT)
    udoc.save()

    udoc.passwordHash = None

    return jsonify(udoc)

@bp.route('/login', methods=['POST'])
@validate(LoginSchema)
def login(data):
    username = data['username']
    password = data['password']
    remember = data['remember']

    udoc = User.objects(username=username).first()
    if not udoc:
        raise Unauthorized('用户名或密码错误')
    if not check_password_hash(udoc.passwordHash, password):
        raise Unauthorized('用户名或密码错误')

    login_user(udoc, remember=remember)

    udoc.passwordHash = None

    return jsonify(udoc)

@bp.route('/logout')
def logout():
    logout_user()
    return jsonify()

@bp.route('/users')
@login_required
def get_users():
    udocs = User.objects.exclude('passwordHash')
    return jsonify(total=0, data=udocs)

@bp.route('/users/<string:username>')
@login_required
def get_user(username):
    udoc = User.objects(username=username).exclude('passwordHash').first()
    if udoc:
        return jsonify(udoc)
    else:
        raise NotFound('用户不存在')

@bp.route('/users/<string:uid>', methods=['PATCH'])
@login_required
def modify_user(uid):
    return 'put' + uid

@bp.route('/status')
@login_required
def user_status():
    udoc = User.objects(id=current_user.get_id()).exclude('passwordHash').first()
    return jsonify(udoc)

# Music
@bp.route('/music')
def get_multiple_music():
    param = QueryMusicParam(request.args)
    if param.validate():
        total = Music.objects.count()

        if param.order.data == 'desc':
            order_by = '-'
        else:
            order_by = '+'

        if param.sort.data == 'date':
            order_by += 'updateDt'
        else:
            order_by += 'views'

        mdocs = Music.objects.order_by(order_by).skip(
            (param.page.data - 1) * param.size.data
        ).limit(
            param.size.data
        )
        return jsonify(total=total, data=mdocs)
    else:
        raise BadRequest('参数错误')

@bp.route('/music', methods=['POST'])
@login_required
@validate(CreateMusicSchema)
def create_music(data):
    title = data['title']
    alias = data['alias']
    author = data['author']
    album = data['album']
    tags = data['tags']
    content = data['content']
    images = data['images']
    references = data['references']

    mdoc = Music(title = title, alias = alias,
                 userId = current_user.get_id(),
                 author = author, album = album,
                 tags = tags, content = content,
                 images = images,
                 references = references)
    mdoc.save()

    return jsonify(mdoc)

@bp.route('/music/<string:mid>')
def get_music(mid):
    if ObjectId.is_valid(mid):
        mdoc = Music.objects(id=mid).first()
        if mdoc:
            return jsonify(mdoc)
    raise NotFound('曲谱不存在')

@bp.route('/music/<string:mid>', methods=['PATCH'])
@login_required
def modify_music(mid):
    pass

# Search

@bp.route('/search')
def ajax_search():
    pass

@bp.route('/search', methods=['POST'])
def search():
    pass
