'''
小程序登录路由文件
'''

from flask import request, json, abort
from ..utils import getAppId, getKeyAndValue
from . import login
from api_1_0 import myRedis
from api_1_0.model import User
from api_1_0 import db


@login.route('/')
def index():
    return json.dumps({'message': 'test seccess'})


@login.route('/login', methods=['POST'])
def _login():
    data = request.json
    data_dict = getAppId(data['code'])
    if data_dict is not None:
        openid = data_dict['openid']
        key, value = getKeyAndValue(data_dict)
        myRedis.set(key, value, ex=60 * 60)
        user = User.query.filter_by(user_id=openid).first()
        if user is None:
            user = User(user_id=openid)
            db.session.add(user)
        return json.dumps({'3rd_session': key})
    else:
        return json.dumps({'error': 'code error'})
