from datetime import datetime
from blue import db
from blue import ma


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    icon = db.Column(db.String(120))
    subcategories = db.relationship('SubCategory', backref='category', lazy='dynamic')
    services = db.relationship('Service', backref='category', lazy='joined')


class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    services_count = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    services = db.relationship('Service', backref='sub_category', lazy='joined')


class Service(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    users = db.relationship('User', backref='service', lazy='joined')


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    identification = db.Column(db.String(15))
    ussid = db.Column(db.String(10))
    photo = db.Column(db.String(10))
    bio = db.Column(db.String(200))
    rating = db.Column(db.String(10))
    status = db.Column(db.String(10))
    type = db.Column(db.String(10))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    locations = db.relationship('Location', backref='service', lazy='joined')


class Location(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    lat = db.Column(db.String(20))
    long = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


class SubCategorySchema(ma.ModelSchema):
    class Meta:
        model = SubCategory


class ServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class LocationSchema(ma.ModelSchema):
    class Meta:
        model = Location
