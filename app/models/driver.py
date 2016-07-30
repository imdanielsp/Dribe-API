import datetime
import json

from app.models.base import db, BaseModel, LAZY
from app.core.tools import ModelHelper, deprecated


class Driver(BaseModel, db.Model):
    """Describes the driver module"""
    __tablename__ = 'driver_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    company = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, date_of_birth, address, email, password, phone_number, company):
        self.driver_id = ModelHelper.get_unique_id()  # Generate a random driver ID
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.address = address
        self.email = email
        self.password = ModelHelper.hash_password(password)
        self.phone_number = phone_number
        self.company = company

    def __repr__(self):
        return "<Driver: ID=%s Name=%s_%s>" % (self.driver_id, self.first_name, self.last_name)
    
    @deprecated
    def update(self, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.date_of_birth = kwargs['date_of_birth']
        self.address = kwargs['address']
        self.email = kwargs['email']
        self.password = ModelHelper.hash_password(kwargs['password'])
        self.phone_number = kwargs['phone_number']
        self.company = kwargs['company']
        db.session.commit()
        return self

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_dict(self):
        return {
                    'id': self.id,
                    'driver_id': self.driver_id,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'date_of_birth': self.date_of_birth.__str__(),
                    'address': self.address,
                    'email': self.email,
                    'password': self.password,
                    'phone_number': self.phone_number,
                    'date_joined': self.date_joined.__str__(),
                    'company': self.company
                }

    @classmethod
    def get_driver_by_id(self, driver_id):
        return Driver.query.filter_by(driver_id=driver_id).first()

    @staticmethod
    def get_all():
        return Driver.query.all()

    @staticmethod
    def build_from_args(**kwargs):
        return Driver(
            kwargs['first_name'], kwargs['last_name'], 
            kwargs['date_of_birth'], kwargs['address'], 
            kwargs['email'], kwargs['password'], 
            kwargs['phone_number'], kwargs['company']
        ).create()


class DriversPool(BaseModel, db.Model):
    __tablename__ = 'drivers_pool'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(255), 
        db.ForeignKey(Driver.__tablename__ + '.driver_id'), nullable=False, unique=True)
    driver = db.relationship(Driver.__name__,
                             backref=db.backref(__tablename__, lazy=LAZY))
    capacity = db.Column(db.Integer, nullable=False)
    current_passengers = db.Column(db.Integer)  # This refer to number of passenger the driver has
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, driver, capacity, latitude, longitude, current_psgr=0):
        self.driver = driver
        self.driver_id = driver.driver_id
        self.capacity = capacity
        self.latitude = latitude
        self.longitude = longitude
        self.current_passengers = current_psgr

    def __repr__(self):
        return "<In Driver Pool: %s>" % self.driver.get_full_name()

    def get_coordinates(self):
        return (self.latitude, self.longitude)

    def get_dict(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'capacity': self.capacity,
            'current_psgr': self.current_passengers,
            'lat': self.latitude,
            'lng': self.longitude
        }

    @staticmethod
    def get_available_driver(request):
        """
        This function return the drivers available to create a ride
        based on the passed request.
        """
        drivers = DriversPool.query.all()
        drivers_available = []
        for driver in drivers:
            if driver.capacity > driver.current_passengers:
                available_seats = driver.capacity - driver.current_passengers
                if available_seats >= request.number_of_passenger:
                    drivers_available.append(driver)
        return drivers_available

    @staticmethod
    def get_by_driver(driver):
        return DriversPool.query.filter_by(driver_id=driver.driver_id).first()

    @staticmethod
    def get_by_driver_id(drv_id):
        return DriversPool.query.filter_by(driver_id=drv_id).first()

    @staticmethod
    def get_by_id(id):
        return DriversPool.query.filter_by(id=id).first()

    @staticmethod
    def build_from_args(**kwargs):
        driver = Driver.get_driver_by_id(kwargs['driver_id'])
        return DriversPool(driver, kwargs['capacity'], kwargs['lat'], kwargs['lng'], kwargs['current_psgr']).create()

    def update_current_capacity(self, n):
        self.current_passengers += n
        db.session.commit()
        return self
