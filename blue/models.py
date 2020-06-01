import datetime
from blue import db
from blue import ma
from flask import current_app as app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    services_count = db.Column(db.String(20))
    service = db.relationship("Service")
    photos = db.relationship("Photos", uselist=False, back_populates="category")


class Service(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    photos = db.relationship("Photos")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="service")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    date_of_birth = db.Column(db.DateTime, default=datetime.datetime.now)
    path_identification = db.Column(db.String(200))
    path_photo = db.Column(db.String(200))
    professional_detail = db.Column(db.String(200))
    service_documentation = db.Column(db.String(200))
    experience = db.Column(db.String(200))
    next_of_kin = db.Column(db.String(200))
    path_business_license = db.Column(db.String(200))


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True)
    service = db.relationship("Service", uselist=False, back_populates="user")

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
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
    service = db.relationship("Service")


class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="photos")
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"))


class MpesaPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    time_stamp = db.Column(db.DateTime, default=datetime.datetime.now)
    amount = db.Column(db.String(10))
    phone_number = db.Column(db.String(10))


class PhotosSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'photo')
        model = Photos


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class ServiceSchema(ma.ModelSchema):
    photos = ma.Nested(PhotosSchema, many=True)

    class Meta:
        model = Service
        fields = ('id', 'description', 'name','description',)


class CategorySchema(ma.ModelSchema):
    photos = ma.Nested(PhotosSchema)

    class Meta:
        fields = ('id', 'name', 'photos',)
        model = Category
