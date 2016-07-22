import datetime
import uuid

from app.models.base import db, BaseModel
from app.core.tools import ModelHelper


class Passenger(BaseModel, db.Model):
    __tablename__ = 'passenger_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passenger_id = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), unique=True)
    date_joined = db.Column(db.DateTime, default=datetime.datetime.now())
    is_active = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, date_of_birth,
                 email, password, phone_number):
        self.passenger_id = ModelHelper.get_unique_id()
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.password = ModelHelper.hash_password(password)
        self.phone_number = phone_number

    def __repr__(self):
        return "<Passenger: %s %s>" % (self.first_name, self.last_name)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
