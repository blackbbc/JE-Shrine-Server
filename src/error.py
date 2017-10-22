# -*- coding: utf-8 -*-

class APIException(Exception):
    status_code = 500
    message = '服务器错误'

    def __init__(self, message):
        if message:
            self.message = message

    def __repr__(self):
        return 'APIException: %s' % self.message

class BadRequest(APIException):
    status_code = 400
    message = '参数非法'

class Unauthorized(APIException):
    status_code = 401
    message = '未登录'

class PermissionDenied(APIException):
    status_code = 402
    message = '没有权限'

class NotFound(APIException):
    status_code = 404
    message = '资源不存在'

class Conflict(APIException):
    status_code = 409
    message = '资源重复'

class UnsupportedMediaType(APIException):
    status_code = 415
    message = '不支持的请求类型'
