'''
资源定义与处理文件
'''

from flask import request, current_app
from flask_restful import Resource, fields, marshal_with
from flask_restful import reqparse

from api_1_0 import myRedis
from api_1_0.decorators import login_required
from api_1_0.model import User, Product
from api_1_0.model import db

# orm模型，用于python对象转json合适数据时的对应关系
from api_1_0.utils import divideOpenIDandSessionKey

resource_fields = {
    'id': fields.Integer,
    'klass': fields.String,
    'title': fields.String,
    'content': fields.String,
    'owner_id': fields.Integer,
    'image_url': fields.String,
    'price': fields.Float,
    'date': fields.DateTime,
}


# 二手商品资源API
class ProductAPI(Resource):

    # 使用restful中的reqparse过滤请求数据
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('klass', type=str, required=True, location='json')
        self.reqparse.add_argument('title', type=str, required=True, location='json')
        self.reqparse.add_argument('content', type=str, required=True, location='json')
        self.reqparse.add_argument('owner_name', type=str, required=True, location='json')
        self.reqparse.add_argument('price', type=str, required=True, location='json')
        super(ProductAPI, self).__init__()

    # 获取资源的API,marshal_with用于将对象转为json格式数据
    @marshal_with(resource_fields)
    def get(self):
        id = request.args.get('id')
        if id is None:
            page = request.args.get('page', 1, type=int)
            pagination = Product.query.order_by(Product.date.desc()).paginate(
                page, per_page=current_app.config['ITEM_PER_PAGE'], error_out=False
            )
            products = pagination.items
            return products
        product = Product.query.filter_by(id=id).first_or_404()
        return product

    # 增加资源的API
    @login_required
    def post(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(name=args.owner_name).first_or_404()
        product = Product(klass=args.klass, title=args.title, content=args.content, owner=user, price=args.price)
        db.session.add_all([user, product])
        return {'message': 'add is ok'}, 201

    # 更新资源的API
    @login_required
    def put(self):
        args = self.reqparse.parse_args()
        product = Product.query.filter_by(id=args.id).first_or_404()
        product.klass = args.klass
        product.title = args.title
        product.content = args.content
        product.price = args.price
        db.session.add(product)
        return {'message': 'change is ok'}

    # 删除资源的API
    @login_required
    def delete(self):
        id = request.args.get('id')
        product = Product.query.filter_by(id=id).first_or_404()
        db.session.delete(product)
        return {'message': 'delete is ok'}


class KlassProductAPI(Resource):
    # 使用restful中的reqparse过滤请求数据
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('klass', type=str, required=True, location='json')
        self.reqparse.add_argument('title', type=str, required=True, location='json')
        self.reqparse.add_argument('content', type=str, required=True, location='json')
        self.reqparse.add_argument('owner_name', type=str, required=True, location='json')
        self.reqparse.add_argument('price', type=str, required=True, location='json')
        super(KlassProductAPI, self).__init__()

    # 获取资源的API,marshal_with用于将对象转为json格式数据
    @marshal_with(resource_fields)
    def get(self):
        klass = request.args.get('klass')
        print(klass)
        if klass is not None:
            page = request.args.get('page', 1, type=int)
            pagination = Product.query.filter_by(klass=klass).order_by(Product.date.desc()).paginate(
                page, per_page=current_app.config['ITEM_PER_PAGE'], error_out=False
            )
            products = pagination.items
            return products
        else:
            return {'error': 'request aruments error'}


class UserProductAPI(Resource):
    # 使用restful中的reqparse过滤请求数据
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('klass', type=str, required=True, location='json')
        self.reqparse.add_argument('title', type=str, required=True, location='json')
        self.reqparse.add_argument('content', type=str, required=True, location='json')
        self.reqparse.add_argument('owner_name', type=str, required=True, location='json')
        self.reqparse.add_argument('price', type=str, required=True, location='json')
        super(UserProductAPI, self).__init__()

    # 获取资源的API,marshal_with用于将对象转为json格式数据
    @login_required
    @marshal_with(resource_fields)
    def get(self):
        rd_session = request.headers.get('3rd_session')
        if rd_session is not None:
            value = myRedis.get(rd_session)
            openid = divideOpenIDandSessionKey(value)
            page = request.args.get('page', 1, type=int)
            pagination = Product.query.filter_by(user_id=openid).order_by(Product.date.desc()).paginate(
                page, per_page=current_app.config['ITEM_PER_PAGE'], error_out=False
            )
            products = pagination.items
            return products
        else:
            return {'error': 'request aruments error'}
