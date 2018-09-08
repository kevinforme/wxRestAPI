'''
工厂函数定义文件
'''

import redis
from flask import Flask
from flask_migrate import Migrate
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# flask插件声明
db = SQLAlchemy()
migrate = Migrate()

# 连接redis并开启连接池(小程序登录)
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
myRedis = redis.Redis(connection_pool=pool)


# 工厂函数
def create_app(config_name):
    # 初始化应用及配置
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化flask插件
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    # 小程序登录蓝本注册
    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)

    # 二手商品资源API注册
    from api_1_0.resources import ProductAPI, KlassProductAPI,UserProductAPI
    api.add_resource(ProductAPI, '/product', endpoint='product')
    api.add_resource(KlassProductAPI, '/klassProduct', endpoint='klassProduct')
    api.add_resource(UserProductAPI, '/userProduct', endpoint='UserProductAPI')

    return app
