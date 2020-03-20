from blue import db
from blue import ma
from flask import current_app as app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

tags = db.Table('tags',
                db.Column('account_id', db.Integer, db.ForeignKey('account.id'), primary_key=True),
                db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
                )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    icon = db.Column(db.String(120))
    subcategories = db.relationship("Subcategory", backref='category', lazy="joined")


class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    services_count = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    accounts = db.relationship("Account")
    service = db.relationship("Service")


class Service(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    photos = db.relationship("Photos")
    user = db.relationship("User")
    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"))
    account = db.relationship("Account", secondary=tags, lazy='subquery',
                              backref=db.backref('service', lazy=True))


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True)
    account = db.relationship("Account")
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
    date_of_birth = db.Column(db.DateTime)
    path_identification = db.Column(db.String)
    path_photo = db.Column(db.String)
    professional_detail = db.Column(db.String)
    service_documentation = db.Column(db.String)
    experience = db.Column(db.String)
    next_of_kin = db.Column(db.String)
    path_business_license = db.Column(db.String)
    is_provider = db.Column(db.Boolean)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Location(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    lat = db.Column(db.String(20))
    long = db.Column(db.String(20))
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship("Account")


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.Boolean)
    bio = db.Column(db.String(250))
    rating = db.Column(db.String(1))
    photos = db.relationship("Photos")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    subcategory_id = db.Column(db.Integer, db.ForeignKey("subcategory.id"))


class ServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service


class SubcategorySchema(ma.ModelSchema):
    service = ma.Nested(ServiceSchema, many=True)

    class Meta:
        model = Subcategory


class CategorySchema(ma.ModelSchema):
    subcategories = ma.Nested(SubcategorySchema, many=True)

    class Meta:
        model = Category


class UserSchema(ma.ModelSchema):
    fields = ("name", "email", "is_provider")

    class Meta:
        model = User


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location


class AccountSchema(ma.ModelSchema):
    class Meta:
        model = Account


class PhotoSchema(ma.ModelSchema):
    class Meta:
        model = Photos
