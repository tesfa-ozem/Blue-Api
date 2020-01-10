from blue import db
from blue import ma
from marshmallow import Schema, fields, pprint

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
    phone = db.Column(db.String(64), unique=True)
    account = db.relationship("Account")
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"))


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


class SubcategorySchema(ma.ModelSchema):
    class Meta:
        model = Subcategory


class CategorySchema(ma.ModelSchema):
    subcategories = ma.Nested(SubcategorySchema, many=True)

    class Meta:
        model = Category


class ServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service


class UserSchema(ma.ModelSchema):
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
