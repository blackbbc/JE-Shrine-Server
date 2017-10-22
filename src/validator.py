# -*- coding: utf-8 -*-

from schema import Schema, Optional, And, Or

RegisterSchema = Schema({
    'username': And(str, len),
    'email': And(str, len),
    'password': And(str, len),
    'password2': And(str, len)
})

LoginSchema = Schema({
    'username': And(str, len),
    'password': And(str, len)
})

CreateMusicSchema = Schema({
    'title': And(str, len),
    Optional('alias'): [And(str, len)],
    Optional('author', default=''): str,
    Optional('album', default=''): str,
    Optional('tags', default=[]): [And(str, len)],
    'content': And(str, len),
    Optional('references', default=[]): [{
        'name': And(str, len),
        'url': And(str, len)
    }]
})
