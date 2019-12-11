from flask import Blueprint, request, jsonify
from blue import db
from blue.models import *
import json

mod = Blueprint('api', __name__)


@mod.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = db.session.query(Category).all()
        category_schema = CategorySchema()
        return json.dumps(category_schema.dump(categories))
    except Exception as e:
        return str(e)


@mod.route('/category', methods=['POST'])
def add_categories():
    name = request.json['name']
    category = Category(name=name, icon='')
    db.session.add(category)
    db.session.commit()
    return 'post'


@mod.route('/subcategory', methods=['POST'])
def add_subcategory():
    name = request.json['name']
    category_id = request.json["category_id"]
    subcategory = SubCategory(name=name, category_id=category_id)
    db.session.add(subcategory)
    db.session.commit()
    return "Successful"
