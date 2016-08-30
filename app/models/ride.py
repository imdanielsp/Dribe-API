import datetime

from app.models.base import db, BaseModel, LAZY
from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.request import Request
from app.core.tools import MathHelper


class Ride(BaseModel, db.Model):
    RIDE_NO_ACCEPTED = 'ride_no_accepted'
    RIDE_PROCESSING = 'ride_processing'
    RIDE_ACTIVE = 'ride_active'
    RIDE_CANCELED = 'ride_cancelled'
    RIDE_COMPLETED = 'ride_completed'

    RIDE_STATUS_LIST = [
        RIDE_NO_ACCEPTED,
        RIDE_PROCESSING,
        RIDE_ACTIVE,
        RIDE_CANCELED,
        RIDE_COMPLETED,
    ]

    __tablename__ = 'ride_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(255), db.ForeignKey(Driver.__tablename__ + '.driver_id'), nullable=False)
    driver = db.relationship('Driver',
                             backref=db.backref(__tablename__, lazy=LAZY))
    passenger_id = db.Column(db.String(255), db.ForeignKey(Passenger.__tablename__ + '.passenger_id'), nullable=False)
    passenger = db.relationship('Passenger',
                                backref=db.backref(__tablename__, lazy=LAZY))
    request_id = db.Column(db.Integer, db.ForeignKey(Request.__tablename__ + '.id'), nullable=False)
    request = db.relationship('Request',
                              backref=db.backref(__tablename__, lazy=LAZY))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.String(30), default=RIDE_NO_ACCEPTED)
    fare_estimate = db.Column(db.Float)

    def __init__(self, request, passenger, driver):
        self.driver = driver
        self.driver_id = driver.driver_id
        self.passenger = passenger
        self.passenger_id = passenger.passenger_id
        self.request = request
        self.request_id = request.id
        self.fare_estimate = MathHelper.calculate_estimate(request)

    def __repr__(self):
        return "<Ride: [Driver: {} Passenger: {} Status: {} Created On: {}]>".format(
            self.driver, self.passenger, self.status, self.created_on
        )

    def get_dict(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'driver': self.driver.__repr__(),
            'passenger_id': self.passenger_id,
            'passenger': self.passenger.__repr__(),
            'request_id': self.request_id,
            'request': self.request.__repr__(),
            'created_on': self.created_on.__str__(),
            'status': self.status,
            'fare_estimate': self.fare_estimate
        }

    def update_status(self, status):
        self.status = status
        db.session.commit()
        return self

    @classmethod
    def get_ride_by_driver(cls, driver):
        return Ride.query.filter_by(driver_id=driver.driver_id).first()

    @staticmethod
    def get_by_id(ride_id):
        return Ride.query.filter_by(id=ride_id).first()

    class InvalidStatus(Exception):
        pass


class CompletedRides(BaseModel, db.Model):
    __tablename__ = 'completed_ride'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ride_id = db.Column(db.Integer, db.ForeignKey(Ride.__tablename__ + ".id"), nullable=False)
    ride = db.relationship(Ride.__name__,
                           backref=db.backref(__tablename__, lazy=LAZY))
    completed_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, ride):
        self.ride = ride
        self.ride_id = ride.id

    def __repr__(self):
        return "<Ride: {} Completed on: {}>".format(self.ride, self.completed_on)


class CancelledRides(BaseModel, db.Model):
    __tablename__ = 'cancelled_ride'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ride_id = db.Column(db.Integer, db.ForeignKey(Ride.__tablename__ + ".id"), nullable=False)
    ride = db.relationship(Ride.__name__,
                           backref=db.backref(__tablename__, lazy=LAZY))
    cancelled_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, ride):
        self.ride = ride
        self.ride_id = ride.id

    def __repr__(self):
        return "<Ride: {} Cancelled on: {}>".format(self.ride, self.cancelled_on)
