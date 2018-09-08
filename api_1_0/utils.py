'''
工具函数文件集
'''

import requests
from flask import jsonify
from werkzeug.security import generate_password_hash


def getAppId(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + 'wx0c26477296bf4958' + '&secret=a8c283d94d1890ecb307beb97bea03c2&js_code=' + code + '&grant_type=authorization_code'
    res = requests.get(url)
    print(res.json())
    if 'openid' in res.json():
        return res.json()
    else:
        return None


def getKeyAndValue(jsobj):
    data = jsobj
    key = generate_password_hash(data['openid'])
    value = data['openid'] + '&' + data['session_key']
    return key, value


def divideOpenIDandSessionKey(value):
    data = value.split('&')
    return data[0]
