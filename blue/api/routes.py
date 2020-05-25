from flask import request, jsonify, send_from_directory, json, abort, url_for, g
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from blue.logic.logic import Logic
from blue.utilities.utilities import *
from blue import create_app
import os
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

mod = Blueprint('api', __name__, url_prefix='/api')

token_auth = HTTPTokenAuth(scheme='Bearer')
basic_auth = HTTPBasicAuth()


# Authentication end points

@mod.route('/token')
@basic_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@basic_auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    print(password)
    print(username_or_token)
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    print(token)
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


@mod.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    if not username or not password or not email:
        return jsonify({'error': 'Missing arguments',
                        'message': 'bad request',
                        'error_code': 400}), 400
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'User exists',
                        'message': 'bad request',
                        'error_code': 400}), 400
    with Logic() as logic:
        logic.add_user(request.json)
        response = jsonify({'error': '',
                            'message': 'User created',
                            'error_code': 201})
        response.status_code = 201
        return response


@mod.route('/user', methods=['PUT'])
def update_user():
    pass


@mod.route('/users', methods=['GET'])
def get_all_users():
    with Logic() as logic:
        return logic.get_all_users()

    return "ok"


# Products Endpoints
@mod.route('/category', methods=['POST'])
def add_category():
    with Logic() as logic:
        logic.add_categories(request.json)

    resp = jsonify({'message': 'Record successfully uploaded'})
    resp.status_code = 201
    return resp


@mod.route('/categories', methods=['GET'])
def get_categories():
    with Logic() as logic:
        return jsonify(logic.get_categories(1))


@mod.route('/photos', methods=['POST'])
def update_photo():
    category_id = request.form['category_id']
    service_id = request.form['service_id']
    if request.method == "POST":
        if request.files:
            time_stamp = str(datetime.datetime.now().strftime("%m-%d-%Y%H:%M:%S"))
            image = request.files["image"]
            with Utilities() as util:
                path = util.save_image(image, time_stamp)
                if not path:
                    return "wrong format"
                else:
                    photo = Photos(photo=path, category_id=category_id, service_id=service_id)
                    db.session.add(photo)
                    db.session.commit()
                    return "Success"

    return "ok"


@mod.route('/service', methods=['POST'])
@token_auth.login_required
def add_service():
    user = g.user
    category_id = request.json["category_id"]
    service = Service(professional_detail="details", name="details", category_id=category_id, user_id=user.id)
    db.session.add(service)
    db.session.commit()
    return "success"


@mod.route('/services', methods=['Get'])
def get_services():
    pass

# @mod.route('/categories', methods=['POST'])
# def get_categories():
#     try:
#         categories = Category.query.order_by(Category.id).all()
#         category_schema = CategorySchema(many=True)
#         resp = jsonify({'count': 1,
#                         'result': category_schema.dump(categories)})
#         resp.status_code = 200
#         return resp
#     except Exception as e:
#         resp = jsonify({'error': str(e.args),
#                         'message': '',
#                         'error_code': 0})
#         return resp
#
#
# @mod.route('/category', methods=['POST'])
# def add_categories():
#     # check if the post request has the file part
#     try:
#         name = request.json['value']['name']
#         category = Category(name=name)
#         db.session.add(category)
#         db.session.commit()
#         resp = jsonify({'message': 'Record successfully uploaded'})
#         resp.status_code = 201
#         return resp
#
#     except Exception as e:
#         resp = jsonify({'error': str(e.args),
#                         'message': '',
#                         'error_code': 0})
#         return resp
#
#
# @mod.route('/user', methods=['POST'])
# def add_user():
#     try:
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         user = User(name=name, phone=phone, email=email)
#         db.session.add(user)
#         db.session.commit()
#         resp = jsonify({'error': '',
#                         'message': 'Successful',
#                         'error_code': 201})
#         resp.status_code = 201
#         return resp
#     except Exception as e:
#         resp = jsonify({'error': str(e.args),
#                         'message': '',
#                         'error_code': 0})
#         return resp
#
#
# @mod.route('/upload_photo', methods=['POST'])
# def upload_photo():
#     pass
#     # if request.method == 'POST' and request.files['image']:
#     #
#     #     # create_app().logger.info(create_app().config['UPLOAD_FOLDER'])
#     #     img = request.files['image']
#     #     image_path = Utilities.save_image(img)
#     #     photo = Photos(photo=image_path, account_id=request.form['account_id'])
#     #     db.session.add(photo)
#     #     db.session.commit()
#     #     return jsonify({'message': 'Photo Uploaded'})
#     # else:
#     #     return jsonify({'message': 'No Image'})
#
#
# @mod.route('/sign_up', methods=['POST'])
# def new_user():
#     try:
#         username = request.json['username']
#         password = request.json['password']
#         full_names = request.json['fullNames']
#         email = request.json['email']
#         if username is None or password is None or email is None:
#             return jsonify({'error': 'Missing arguments',
#                             'message': 'bad request',
#                             'error_code': 400}), 400
#         if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first() is not None:
#             return jsonify({'error': 'User exists',
#                             'message': 'bad request',
#                             'error_code': 400}), 400
#         user = User(username=username, email=email, name=full_names)
#         user.hash_password(password)
#         db.session.add(user)
#         db.session.commit()
#         response = jsonify({'error': '',
#                             'message': 'User created',
#                             'error_code': 201})
#         response.status_code = 201
#         return response
#     except Exception as e:
#         resp = jsonify({'error': str(e),
#                         'message': '',
#                         'error_code': 404})
#         resp.status_code = 404
#         return resp
#
#
# @mod.route('/token', methods=['POST'])
# @auth.login_required
# def get_auth_token():
#     token = g.user.generate_auth_token()
#     return jsonify({'token': token.decode('ascii')})
#
#
# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username=username_or_token).first()
#         if not user or not user.verify_password(password):
#             return False
#     g.user = user
#     return True
#
#
# # @mod.route('/registerProvider', methods=['POST'])
# # @auth.login_required
# # def register_provider():
# #     # TODO fix dates and file uploads
# #     try:
# #         data = request.data
# #         print(str(data))
# #         # file = request.files['file']
# #         date_of_birth = datetime.datetime.strptime('08-04-1994', '%m-%d-%Y')
# #         identification_path = ''
# #         # if file.filename == '':
# #         #     resp = jsonify({'message': 'No file selected for uploading'})
# #         #     resp.status_code = 400
# #         #     return resp
# #         # if file and Utilities.allowed_file(file.filename):
# #         #     identification = request.files['file']
# #         #     identification_path = Utilities.save_image(identification, "identification")
# #         user_logged = g.user.username
# #         user = User.query.filter_by(username=user_logged).first()
# #         user.date_of_birth = date_of_birth
# #         user.name = request.json['name']
# #         user.phone = request.json['phone']
# #         user.service_id = request.json['service_id']
# #         user.professional_detail = request.json['professional_detail']
# #         user.experience = request.json['experience']
# #         user.next_of_kin = request.json['next_of_kin']
# #         user.service_documentation = request.json['service_documentation']
# #         user.path_identification = identification_path
# #         user.is_provider = request.json['is_provider']
# #         db.session.add(user)
# #         db.session.commit()
# #         resp = jsonify({'message': 'Record successfully retrived',
# #                         "data": ""})
# #         resp.status_code = 200
# #         return resp
# #     except Exception as e:
# #         resp = jsonify({'error': str(e.args),
# #                         'message': '',
# #                         'error_code': 0})
# #         return resp
#
#
# @mod.route('/login', methods=['POST'])
# @auth.login_required
# def login():
#     resp = jsonify({'message': 'Logged In'})
#     resp.status_code = 200
#     return resp
