# -*- coding: utf-8 -*-

import datetime
from bson.objectid import ObjectId

import flask_login
from flask_mongoengine import MongoEngine

from error import Unauthorized

db = MongoEngine()
login_manager = flask_login.LoginManager()

class Tag(db.Document):
    name = db.StringField(required=True)

class User(db.Document):
    username = db.StringField(required=True)
    passwordHash = db.StringField(required=True)
    email = db.StringField(required=True)
    role = db.IntField(required=True)
    avatar = db.StringField()

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Music(db.Document):
    title = db.StringField(required=True)
    alias = db.ListField(db.StringField())
    userId = db.ObjectIdField(required=True)
    author = db.StringField()
    album = db.StringField()
    tags = db.DictField()
    content = db.StringField(required=True)
    createDt = db.DateTimeField(required=True, default=datetime.datetime.now)
    updateDt = db.DateTimeField(required=True, default=datetime.datetime.now)
    images = db.DictField()
    references = db.ListField(db.DictField())
    viewCount = db.IntField(required=True)
    statuc = db.IntField(required=True)

class Star(db.Document):
    userId = db.ObjectIdField(required=True)
    name = db.StringField(required=True)
    music = db.ListField(db.ObjectIdField())
    createDt = db.DateTimeField(required=True, default=datetime.datetime.now)
    updateDt = db.DateTimeField(required=True, default=datetime.datetime.now)

@login_manager.user_loader
def user_loader(uid):
    return User.objects(id=ObjectId(uid)).first()

@login_manager.unauthorized_handler
def unauthorized():
    raise Unauthorized('未登录')
