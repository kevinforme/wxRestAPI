'''
数据库模型定义文件
'''

from datetime import datetime

from api_1_0 import db

# 用户感兴趣的商品与关注某商品的用户之间的关联表
registrations = db.Table('registrations',
                         db.Column('User_id', db.Integer, db.ForeignKey('products.id')),
                         db.Column('class_id', db.Integer, db.ForeignKey('users.id'))
                         )


# 用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    products = db.relationship('Product', backref='owner', lazy='dynamic')
    like = db.relationship('Product', secondary=registrations, backref=db.backref('users', lazy='dynamic'),
                           lazy='dynamic')

    def to_json(self):
        json_user = {
            'name': self.name
        }
        return json_user


# 二手商品模型
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    klass = db.Column(db.String(32), index=True, nullable=False)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_url = db.Column(db.String(128))
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    state = db.Column(db.Boolean, default=0)

    def to_json(self):
        json_product = {
            'klass': self.klass,
            'title': self.title,
            'content': self.content,
            'owner_id': self.owner_id,
            'image_url': self.image_url,
            'price': self.price,
            'date': self.date,
            'state': self.state,
            'like': self.users.count()
        }
        return json_product
