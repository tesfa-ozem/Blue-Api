import json

from flask import jsonify, g
from sqlalchemy import func

from blue import db

import numpy as np
import pandas as pd

from blue.models import *


class Logic:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(exc_type)

    def get_customers(self):
        try:
            user_count = User.query.filter(User.is_provider is not True).count()
            return user_count
        except:
            pass

    def get_paymemts(self):
        try:
            amount = db.session.query(
                func.sum(MpesaPayment.amount)
            ).scalar()
            return str(amount)
        except:
            pass

    def get_revenue(self):
        pass

    def get_today_sales(self):
        pass

    def get_current_week_sales(self):
        try:
            dates = pd.date_range('20130101', periods=6)

            payments = db.session.query(MpesaPayment.name, MpesaPayment.time_stamp, MpesaPayment.amount).all()
            df = pd.DataFrame(payments)
            # df['day'] = pd.to_datetime(df['time_stamp'])

            return df
        except Exception as e:
            pass

    def get_last_week_sales(self):
        pass

    def get_sales_service(self):
        pass

    def get_top_selling(self):
        pass

    def get_orders(self):
        pass

    def get_sale_location(self):
        pass

    def get_all_users(self):
        try:
            users = db.session.query(User).all()
            user_schema = UserSchema(many=True)
            return jsonify(user_schema.dump(users))
        except:
            pass

    def get_categories(self, page_id):
        categories = Category.query.order_by(Category.id).paginate(page_id, 5, False)
        categories_schema = CategorySchema(many=True)
        data = categories_schema.dump(categories.items)
        print(data)
        return [{x: y['photo'] if 'photos' == x and i['photos'] is not None else y for x, y in i.items()} for i in data]

    def update_categories(self, args):
        categories = Category.query.filter(Category.id == args.id)
        categories.name = args.name
        categories.description = args.description
        categories.icon = args.icon
        db.session.add(categories)
        db.session.commit()

    def add_categories(self, args):
        name = args['value']['name']
        print(name)
        categories = Category(name=name)
        db.session.add(categories)
        db.session.commit()

    def add_user(self, args):
        user = User(username=args['username'], email=args['email'], name=args['names'])
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()

    def create_service(self, args):
        user = g.user
        service = Service(name=args['name'], description=args['description'], user_id=user.id,
                          category_id=args['category_id'], )
        db.session.add(service)
        db.session.commit()

    def get_service(self, args):
        service = Service.query.filter(Service.category_id == args['category_id']).order_by(Service.id).paginate(
            args['page_id'], 5, False)
        service_schema = ServiceSchema(many=True)
        data = service_schema.dump(service.items)
        return data

    def list_service(self, page_id):
        service_list = Service.query.order_by(Service.id).paginate(page_id, 5, False)
        return service_list
