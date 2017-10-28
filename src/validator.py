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

CreateMusicSchema = Schema({
    'title': And(str, len),
    Optional('alias', default=[]): [And(str, len)],
    Optional('author', default=''): str,
    Optional('album', default=''): str,
    Optional('tags', default=[]): [And(str, len)],
    'content': And(str, len),
    'images': {
        'small': And(str, len),
        'large': And(str, len)
    },
    Optional('references', default=[]): [{
        'name': And(str, len),
        'url': And(str, len)
    }]
})

class QueryMusicParam(FlaskForm):
    page = IntegerField('Page', [validators.Optional(), validators.NumberRange(min=1)], default=1)
    size = IntegerField('Size', [validators.Optional(), validators.NumberRange(min=1)], default=10)
    sort = StringField('Sort By', [validators.Optional(), validators.AnyOf(['date', 'views'])], default='date')
    order = StringField('Order By', [validators.Optional(), validators.AnyOf(['asc', 'desc'])], default='desc')
