from blue import db
from blue import ma


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    icon = db.Column(db.String(120))
    subcategories = db.relationship("SubCategory", backref='category', lazy="joined")


class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    services_count = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))


class Service(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    photos = db.relationship("Photos")
    user = db.relationship("User")
    subcategory_id = db.Column(db.Integer, db.ForeignKey("sub_category.id"))


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
    photo = db.Column(db.String())
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"))
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.Boolean)
    bio = db.Column(db.String())
    rating = db.Column(db.String())
    photos = db.relationship("Photos")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")


class SubCategorySchema(ma.ModelSchema):
    class Meta:
        model = SubCategory


class CategorySchema(ma.ModelSchema):
    subcategory = ma.Nested(SubCategorySchema(), many=True)

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
