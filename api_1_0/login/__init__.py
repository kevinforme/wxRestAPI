'''
小程序登录蓝本定义与路由整合文件
'''

from flask import Blueprint

login = Blueprint('login', __name__)

from . import view
