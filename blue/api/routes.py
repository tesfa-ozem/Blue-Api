import json
import os
from flask import current_app, Blueprint, request, jsonify
from sqlalchemy.orm import joinedload

from blue.models import *
from werkzeug.utils import secure_filename
from blue.utilities.utilities import *

mod = Blueprint('api', __name__)


@mod.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.order_by(Category.id).outerjoin(SubCategory).all()
        category_schema = CategorySchema(many=True)
        for row in categories[1].subcategories:
            print(row.__dict__)
        return json.dumps(category_schema.dump(categories))
    except Exception as e:
        return str(e)


@mod.route('/category', methods=['POST'])
def add_categories():
    # check if the post request has the file part
    try:
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and Utilities.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name = request.form['name']
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            resp = jsonify({'message': 'Record successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp
    except Exception as e:
        return str(e)


@mod.route('/subcategory', methods=['POST'])
def add_subcategory():
    try:
        name = request.form['name']
        category_id = request.form["category_id"]
        subcategory = SubCategory(name=name, category_id=category_id)
        db.session.add(subcategory)
        db.session.commit()
        resp = jsonify({'message': 'Record successfully uploaded'})
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route('/subcategory', methods=['GET'])
def get_subcategories():
    try:
        subcategories = SubCategory.query.order_by(SubCategory.id).all()
        subcatagory_schema = SubCategorySchema(many=True)
        return jsonify(subcatagory_schema.dump(subcategories))
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route('/service', methods=['POST'])
def add_service():
    try:
        name = request.form['name']
        description = request.form['description']
        photos = request.form['photos']
        subcategory_id = request.form['subcategory_id']
        service = Service(name=name, description=description, photos=photos, subcategory_id=subcategory_id)
        db.session.add(service)
        db.session.commit()
        resp = jsonify({'message': 'Record successfully uploaded'})
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route('/user', methods=['POST'])
def add_user():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        user = User(name=name, phone=phone, email=email)
        db.session.add(user)
        db.session.commit()
        resp = jsonify({'message': 'Record successfully uploaded'})
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route('/account', methods=['POST'])
def add_account():
    try:
        provider = request.form['provider']
        bio = request.form['bio']
        rating = request.form['rating']
        photos = request.form['photos']
        user_id = request.form['user_id']

        account = Account(provider=provider, bio=bio, rating=rating, photos=photos, user_id=user_id)
        db.session.add(account)
        db.session.commit()
        resp = jsonify({'message': 'Record successfully uploaded'})
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp

