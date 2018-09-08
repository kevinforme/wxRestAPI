'''
应用程序配置文件
'''

# 通用配置类
class Config:
    SECRET_KEY = 'hard_guess_!@#$%^&*()_+'

    # 数据库sqlalchemy相关配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_TIMEOUT = True

    # 项目参数配置
    ITEM_PER_PAGE = 10

    # 帮助初始化程序的方法（工厂函数中调用）
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置类
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qwer@localhost:3306/wxrest_dev'


# 生产环境配置类
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qwer@localhost:3306/wxrest_pro'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
