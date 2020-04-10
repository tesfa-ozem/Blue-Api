from flask import request, jsonify, send_from_directory, json, abort, url_for, g
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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
        return resp


@mod.route('/category', methods=['POST'])
def add_categories():
    # check if the post request has the file part
    try:
        # if 'icon' not in request.files:
        #     resp = jsonify({'message': 'No file part in the request'})
        #     resp.status_code = 400
        #     return resp
        file = request.files['icon']
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and Utilities.allowed_file(file.filename):
            icon = request.files['icon']
            icon_path = Utilities.save_image(icon, "Category")
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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
        return resp


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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
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
        resp = jsonify({'error': str(e.args),
                        'message': str(e.args),
                        'error_code': 0})
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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
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
        resp = jsonify({'error': '',
                        'message': 'Successful',
                        'error_code': 201})
        resp.status_code = 201
        return resp
    except Exception as e:
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
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
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
        return resp


@mod.route("/service", methods=['GET'])
def get_services():
    try:
        if request.args.get('service_id') is not None:
            service_id = request.args.get('service_id')
            service = Service.query.filter(Service.id == service_id).one()
            service_schema = ServiceSchema()
            resp = jsonify({'message': 'Record successfully retrived',
                            "data": service_schema.dump(service)})
            resp.status_code = 200
            return resp
        else:
            service = Service.query.order_by(Service.id).all()
            service_schema = ServiceSchema(many=True)
            resp = jsonify({'message': 'Record successfully retrived',
                            "data": service_schema.dump(service)})
            resp.status_code = 200
            return resp
    except Exception as e:
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
        return resp


@mod.route('/sign_up', methods=['POST'])
def new_user():
    try:
        print(request.data)
        username = request.json['username']
        password = request.json['password']
        full_names = request.json['fullNames']
        email = request.json['email']
        if username is None or password is None or email is None:
            return jsonify({'error': 'Missing arguments',
                            'message': 'bad request',
                            'error_code': 400}), 400
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email) is not None:
            return jsonify({'error': 'User exists',
                            'message': 'bad request',
                            'error_code': 400}), 400
        user = User(username=username, email=email, name=full_names)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username}), 201, {
            'User': 'Is created'}
    except Exception as e:
        resp = jsonify({'error': e,
                        'message': '',
                        'error_code': 400}), 400
        return resp


@mod.route('/token', methods=['POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@mod.route('/registerProvider', methods=['POST'])
@auth.login_required
def register_provider():
    # TODO fix dates and file uploads
    try:
        data = request.data
        print(str(data))
        # file = request.files['file']
        date_of_birth = datetime.datetime.strptime('08-04-1994', '%m-%d-%Y')
        identification_path = ''
        # if file.filename == '':
        #     resp = jsonify({'message': 'No file selected for uploading'})
        #     resp.status_code = 400
        #     return resp
        # if file and Utilities.allowed_file(file.filename):
        #     identification = request.files['file']
        #     identification_path = Utilities.save_image(identification, "identification")
        user_logged = g.user.username
        user = User.query.filter_by(username=user_logged).first()
        user.date_of_birth = date_of_birth
        user.name = request.json['name']
        user.phone = request.json['phone']
        user.service_id = request.json['service_id']
        user.professional_detail = request.json['professional_detail']
        user.experience = request.json['experience']
        user.next_of_kin = request.json['next_of_kin']
        user.service_documentation = request.json['service_documentation']
        user.path_identification = identification_path
        user.is_provider = request.json['is_provider']
        db.session.add(user)
        db.session.commit()
        resp = jsonify({'message': 'Record successfully retrived',
                        "data": ""})
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
        return resp


@mod.route('/login', methods=['POST'])
@auth.login_required
def login():
    resp = jsonify({'message': 'Logged In'})
    resp.status_code = 200
    return resp


@mod.route('/getProvider', methods=['POST'])
@auth.login_required
def get_provider():
    try:
        user_logged = g.user
        user_schema = UserSchema()
        resp = jsonify({'message': 'Record successfully retried',
                        "data": user_schema.dump(user_logged)})
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify({'error': str(e.args),
                        'message': '',
                        'error_code': 0})
        return resp


@mod.route('getUser', methods=['POST'])
@auth.login_required
def get_user():
    user = g.user
    return jsonify({
        'data': user
    })
