# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, StringField
from schema import Schema, Optional, And, Or

RegisterSchema = Schema({
    'username': And(str, len),
    'email': And(str, len),
    'password': And(str, len),
    'password2': And(str, len)
})

LoginSchema = Schema({
    'username': And(str, len),
    'password': And(str, len),
    'remember': bool
})

ModifyUserSchema = Schema({
    Optional('password'): And(str, len),
    Optional('email'): And(str, len),
    Optional('role'): And(int, Or(10, 20, 30)),
    Optional('avatar'): And(str, len)
})

CreateMusicSchema = Schema({
    'title': And(str, len),
    Optional('alias', default=[]): [And(str, len)],
    Optional('author', default=''): str,
    Optional('composer', default=''): str,
    Optional('singer', default=''): str,
    Optional('album', default=''): str,
    Optional('tags', default=[]): [And(str, len)],
    'content': And(str, len),
    'cover': And(str, len),
    Optional('references', default=[]): [{
        'name': And(str, len),
        'url': And(str, len)
    }]
})

ModifyMusicSchema = Schema({
    Optional('title'): And(str, len),
    Optional('alias'): [And(str, len)],
    Optional('author'): And(str, len),
    Optional('composer'): And(str, len),
    Optional('singer'): And(str, len),
    Optional('album'): And(str, len),
    Optional('tags'): [And(str, len)],
    Optional('content'): And(str, len),
    Optional('cover'): And(str, len),
    Optional('references'): [{
        'name': And(str, len),
        'url': And(str, len)
    }],
    Optional('status'): And(int, Or(0, 1))
})

class QueryMusicParam(FlaskForm):
    page = IntegerField('Page', [validators.Optional(), validators.NumberRange(min=1)], default=1)
    size = IntegerField('Size', [validators.Optional(), validators.NumberRange(min=1)], default=10)
    sort = StringField('Sort By', [validators.Optional(), validators.AnyOf(['date', 'views'])], default='date')
    order = StringField('Order By', [validators.Optional(), validators.AnyOf(['asc', 'desc'])], default='desc')

class SearchMusicParam(FlaskForm):
    q = StringField('Keyword', [validators.Optional(), validators.Length(min=1)])
    page = IntegerField('Page', [validators.Optional(), validators.NumberRange(min=1)], default=1)
    size = IntegerField('Size', [validators.Optional(), validators.NumberRange(min=1)], default=10)
