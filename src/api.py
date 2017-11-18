# -*- coding: utf-8

import uuid
from functools import wraps
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from flask import Blueprint, jsonify, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from schema import SchemaError

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

import builtin
from util import mail
from error import APIException, BadRequest, Unauthorized, PermissionDenied, NotFound, Conflict
from model import Music, Star, Tag, User, Authorization, login_manager
from validator import RegisterSchema, LoginSchema, CreateMusicSchema, QueryMusicParam, \
                      ModifyMusicSchema, ModifyUserSchema, SearchMusicParam

bp = Blueprint('api', __name__)

es = Elasticsearch()

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

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            udoc = User.objects(id=current_user.get_id()).first()
            if udoc.role >= role:
                return func(*args, **kwargs)
            else:
                raise PermissionDenied('没有权限使用该API')
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

    udoc = User(username=username, nickname=username, password=generate_password_hash(password),
                email=email, role=builtin.ROLE_UNAUTHORIZED)
    udoc.save()

    code = uuid.uuid4().hex
    adoc = Authorization(email=email, code=code)
    adoc.save()
    mail.sendTo(email, '验证电子邮件地址', '感谢您注册自由神社账户\n\n点击此链接验证您的电子邮件 \
            \n\n%s://%s/api/verify?code=%s\n' % (request.scheme, request.host, code))

    udoc.password = None

    return jsonify(udoc)

@bp.route('/verify')
def verify():
    code = request.args.get('code', None)

    if code:
        adoc = Authorization.objects(code=code).order_by('-time').first()
        if adoc and adoc.time - datetime.now() < timedelta(hours=1):
            udoc = User.objects(email=adoc.email).first()
            if udoc.role == builtin.ROLE_UNAUTHORIZED:
                udoc.role = builtin.ROLE_DEFAULT
                udoc.save()

            # udoc.password = None

            return jsonify()
        else:
            raise BadRequest('验证码已失效')
    else:
        raise BadRequest('链接无效')

@bp.route('/verify/send')
def send_verify_email():
    email = request.args.get('email', None)

    if email:
        udoc = User.objects(email=email).first()
        if udoc:
            code = uuid.uuid4().hex
            adoc = Authorization(email=email, code=code)
            adoc.save()
            mail.sendTo(email, '验证电子邮件地址', '感谢您注册自由神社账户\n\n点击此链接验证您的电子邮件 \
                    \n\n%s://%s/api/verify?code=%s\n' % (request.scheme, request.host, code))

            return jsonify()
        else:
            raise NotFound('用户不存在')
    else:
        raise BadRequest('链接无效')

@bp.route('/login', methods=['POST'])
@validate(LoginSchema)
def login(data):
    username = data['username']
    password = data['password']
    remember = data['remember']

    udoc = User.objects(username=username).first()
    if not udoc:
        raise Unauthorized('用户名或密码错误')
    if not check_password_hash(udoc.password, password):
        raise Unauthorized('用户名或密码错误')

    login_user(udoc, remember=remember)

    udoc.password = None

    return jsonify(udoc)

@bp.route('/logout')
def logout():
    logout_user()
    return jsonify()

@bp.route('/users')
@login_required
def get_users():
    udocs = User.objects.exclude('password')
    return jsonify(total=0, data=udocs)

@bp.route('/users/<string:username>')
@login_required
def get_user(username):
    udoc = User.objects(username=username).exclude('password').first()
    if udoc:
        return jsonify(udoc)
    else:
        raise NotFound('用户不存在')

@bp.route('/users/<string:uid>', methods=['PATCH'])
@login_required
@role_required(builtin.ROLE_ADMIN)
@validate(ModifyUserSchema)
def modify_user(data, uid):
    if ObjectId.is_valid(uid):
        udoc = User.objects(id=uid).first()
        if udoc:
            for name, value in data.items():
                if 'name' == 'password':
                    udoc.password = generate_password_hash(value)
                else:
                    setattr(udoc, name, value)
            udoc.save()

            udoc.password = None

            return jsonify(udoc)
    raise NotFound('用户不存在')

@bp.route('/status')
@login_required
def user_status():
    udoc = User.objects(id=current_user.get_id()).exclude('password').first()
    return jsonify(udoc)

# Music
@bp.route('/music')
def get_multiple_music():
    param = QueryMusicParam(request.args)
    if param.validate():

        if param.order.data == 'desc':
            order_by = '-'
        else:
            order_by = '+'

        if param.sort.data == 'date':
            order_by += 'updateDt'
        else:
            order_by += 'views'

        tag = param.tag.data
        if tag:
            mdocs = Music.objects(tags=tag)
        else:
            mdocs = Music.objects

        total = mdocs.count()

        mdocs = mdocs.order_by(order_by).skip(
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
    mdoc = Music(userId = current_user.get_id(), **data)
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
@role_required(builtin.ROLE_VIP)
@validate(ModifyMusicSchema)
def modify_music(data, mid):
    if ObjectId.is_valid(mid):
        mdoc = Music.objects(id=mid).first()
        if mdoc:
            for name, value in data.items():
                setattr(mdoc, name, value)
            mdoc.updateDt = datetime.now()
            mdoc.save()

            return jsonify(mdoc)
    raise NotFound('曲谱不存在')

# Search

@bp.route('/suggest')
def suggest():
    if 'term' in request.args and request.args['term']:
        term = request.args['term']

        s = Search(using=es, index='je-shrine') \
                .query('match_phrase_prefix', title=term)

        res = s.execute()

        data = [ hit.title for hit in res[0:10] ]

        return jsonify(data)
    else:
        return jsonify([])

@bp.route('/search')
def search():
    param = SearchMusicParam(request.args)
    if param.validate():
        q = param.q.data
        page = param.page.data
        size = param.size.data

        s = Search(using=es, index='je-shrine') \
                .query(MultiMatch(
                    query=q,
                    fields=['title', 'alias', 'author', 'album', 'tags']
                    ))

        res = s.execute()

        total = res.hits.total

        data = []

        for hit in res[(page - 1) * size: page * size]:
            item = hit.to_dict()
            item['id'] = hit.meta.id
            data.append(item)

        return jsonify(total=total, data=data)

    else:
        raise BadRequest('参数错误')
