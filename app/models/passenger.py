import datetime
import uuid

from app.models.base import db, BaseModel
from app.core.tools import ModelHelper, deprecated


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

    @deprecated
    def update(self, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.date_of_birth = kwargs['date_of_birth']
        self.email = kwargs['email']
        self.password = ModelHelper.hash_password(kwargs['password'])
        self.phone_number = kwargs['phone_number']
        db.session.commit()
        return self

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_dict(self):
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'email': self.email,
            'password': self.password,
            'phone_number': self.password,
            'date_joined': self.date_joined,
            'is_active': self.is_active
        }

    @staticmethod
    def build_from_args(**kwargs):
        return Passenger(
            kwargs['first_name'], 
            kwargs['last_name'], 
            kwargs['date_of_birth'], 
            kwargs['email'], 
            kwargs['password'], 
            kwargs['phone_number']
        ).create()

    @staticmethod
    def get_by_id(passenger_id):
        return Passenger.query.filter_by(passenger_id=passenger_id).first()

    @staticmethod
    def get_all():
        return Passenger.query.all()
