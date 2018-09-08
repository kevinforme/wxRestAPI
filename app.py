'''
应用程序入口文件
'''

from api_1_0 import db
from api_1_0 import create_app
from api_1_0.model import User, Product

import os

# 应用入口
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


# shell环境全局变量声明
@app.shell_context_processor
def make_shell_context():
    return dict(User=User, Product=Product, db=db)


# 部署程序
@app.cli.command()
def deploy():
    """deploy app"""
    from flask_migrate import upgrade

    upgrade()
