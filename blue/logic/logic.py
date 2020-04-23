from flask import jsonify
from sqlalchemy import func

from blue import db

import numpy as np
import pandas as pd

from blue.models import *


class Logic:

    def get_customers(self):
        user_count = User.query.filter(User.is_provider is not True).count()
        return user_count

    def get_paymemts(self):
        amount = db.session.query(
            func.sum(MpesaPayment.amount)
        ).scalar()
        return str(amount)

    def get_revenue(self):
        pass

    def get_today_sales(self):
        pass

    def get_current_week_sales(self):
        dates = pd.date_range('20130101', periods=6)

        payments = db.session.query(MpesaPayment.name, MpesaPayment.time_stamp, MpesaPayment.amount).all()
        df = pd.DataFrame(payments)
        df['day'] = pd.to_datetime(df['time_stamp'])

        return df

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
        users = db.session.query(User).all()
        user_schema = UserSchema(many=True)
        return jsonify(user_schema.dump(users))
