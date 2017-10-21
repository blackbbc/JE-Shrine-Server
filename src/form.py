# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('用户名为空')])
    email = StringField('Email', validators=[Email('邮箱格式非法')])
    password = StringField('Password', validators=[DataRequired('密码为空'), Length(min=6, message='密码必须大于等于6位')])
    password2 = StringField('Password again', validators=[DataRequired('密码为空')])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired('用户名为空')])
    password = StringField('password', validators=[DataRequired('用户名为空')])
