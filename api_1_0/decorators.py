'''
装饰器工具文件
'''
import functools

from flask import request

from api_1_0 import myRedis


def login_required(fn):
    @functools.wraps(fn)
    def wrap(*args, **kwargs):
        rd_session = request.headers.get('3rd_session')
        session_value = myRedis.get(rd_session)
        if session_value is None:
            return {'exception': 'login plz'}, 403
        return fn(*args, **kwargs)

    return wrap
