import datetime

from flask import jsonify

from app.models.base import db, BaseModel
from app.models.tools import ModelHelper


class Driver(BaseModel, db.Model):
    """Describes the driver module"""
    __tablename__ = 'driver_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    company = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, date_of_birth, email, password, company):
        self.driver_id = ModelHelper.get_unique_id()  # Generate a random driver ID
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = ModelHelper.hash_password(password)
        self.company = company

    def __repr__(self):
        return "<Driver: ID=%s Name=%s_%s>" % (self.driver_id, self.first_name, self.last_name)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


        return jsonify(
            driver_api_id=self.driver_id,
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=self.date_of_birth,
            email=self.email,
            password=self.password,
            company=self.company
        )

    @staticmethod
    def build_from_arg(**kwargs):
        return Driver(kwargs["first_name"], kwargs["last_name"],
                      kwargs["date_of_birth"], kwargs["email"],
                      kwargs["password"], kwargs["company"])


class DriversPool(BaseModel, db.Model):
    __tablename__ = 'drivers_pool'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(255), db.ForeignKey(Driver.__tablename__ + '.driver_id'), nullable=False)
    driver = db.relationship(Driver.__name__,
                             backref=db.backref(__tablename__, lazy='dynamic'))
    capacity = db.Column(db.Integer, nullable=False)

    def __init__(self, driver):
        self.driver = driver

    def __repr__(self):
        return "<In Driver Pool: %s>" % self.driver.get_full_name()
