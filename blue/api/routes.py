from flask import request, jsonify, send_from_directory, json
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from blue.utilities.utilities import *
from blue import create_app
import os
from flask_httpauth import HTTPBasicAuth

mod = Blueprint('api', __name__, url_prefix='/api')

auth = HTTPBasicAuth()


@mod.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.order_by(Category.id).options(joinedload('subcategories')).all()
        category_schema = CategorySchema(many=True)
        resp = jsonify({'message': 'Record successfully retried',
                        "data": category_schema.dump(categories)})
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route('/category', methods=['POST'])
def add_categories():
    # check if the post request has the file part
    try:
        if 'icon' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['icon']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and Utilities.allowed_file(file.filename):
            icon = request.files['icon']
            icon_path = Utilities.save_image(icon)
            name = request.form['name']
            category = Category(name=name, icon=icon_path)
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
        subcategory = Subcategory(name=name, category_id=category_id)
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
        subcategories = Subcategory.query.order_by(Subcategory.id).all()
        subcatagory_schema = SubcategorySchema(many=True)
        resp = jsonify({'message': 'Record successfully retried',
                        "data": subcatagory_schema.dump(subcategories)})
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route('/service', methods=['POST'])
def add_service():
    try:
        name = request.form['name']
        description = request.form['description']
        subcategory_id = request.form['subcategory_id']
        service = Service(name=name, description=description, subcategory_id=subcategory_id)
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
        user_id = request.form['user_id']

        account = Account(provider=True, bio=bio, rating=rating, user_id=user_id)
        db.session.add(account)
        db.session.commit()
        resp = jsonify({'message': 'Record successfully uploaded'})
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route("/subcategory", methods=['GET'])
def get_subcategory():
    try:
        category_id = request.args.get('category_id')
        subcategory = Subcategory.query.filter(Subcategory.category_id == category_id).one()
        subcategory_schema = SubcategorySchema(many=True)
        resp = jsonify({'message': 'Record successfully retried',
                        "data": jsonify(subcategory_schema.dump(subcategory))})
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
        return resp


@mod.route("/linkAccount", methods=['POST'])
def upadate_account():
    account_id = request.form['account_id']
    account = Account.query.filter(Account.id == add_account).one()


@mod.route('/upload_photo', methods=['POST'])
def upload_photo():
    if request.method == 'POST' and request.files['image']:

        # create_app().logger.info(create_app().config['UPLOAD_FOLDER'])
        img = request.files['image']
        image_path = Utilities.save_image(img)
        photo = Photos(photo=image_path, account_id=request.form['account_id'])
        db.session.add(photo)
        db.session.commit()
        return jsonify({'message': 'Photo Uploaded'})
    else:
        return jsonify({'message': 'No Image'})


@mod.route("/account", methods=['GET'])
def get_account():
    try:
        if request.args.get('id') != '':
            account_id = request.args.get('id')
            account = Account.query.filter(Account.id == account_id).one()
            account_schema = AccountSchema()
            resp = jsonify({'message': 'Record successfully retried',
                            "data": account_schema.dump(account)})
            resp.status_code = 200
            return resp
        else:
            account = Account.query.order_by(Account.id).all()
            account_schema = AccountSchema(many=True)
            resp = jsonify({'message': 'Record successfully retried',
                            "data": account_schema.dump(account)})
            resp.status_code = 200
            return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
    return resp


@mod.route("/service", methods=['GET'])
def get_services():
    try:
        if request.args.get('id') != '':
            service_id = request.args.get('service_id')
            service = Service.query.filter(Service.id == service_id).one()
            service_schema = ServiceSchema()
            resp = jsonify({'message': 'Record successfully retried',
                            "data": service_schema.dump(service)})
            resp.status_code = 200
            return resp
        else:
            service = Service.query.order_by(Service.id).all()
            service_schema = ServiceSchema(many=True)
            resp = jsonify({'message': 'Record successfully retried',
                            "data": service_schema.dump(service)})
            resp.status_code = 200
            return resp
    except Exception as e:
        resp = jsonify({'Error': str(e.args)})
    return resp

