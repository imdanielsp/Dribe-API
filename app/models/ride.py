import datetime

from app.models.base import db, BaseModel
from app.core.tools import MathHelper


class Ride(BaseModel, db.Model):
    RIDE_NO_ACCEPTED = 'ride_no_accepted'
    RIDE_PROCESSING = 'ride_processing'
    RIDE_ACTIVE = 'ride_active'
    RIDE_CANCELED = 'ride_cancelled'
    RIDE_COMPLETED = 'ride_completed'

    __tablename__ = 'ride_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(255), db.ForeignKey('driver_info.driver_id'))
    driver = db.relationship('Driver',
                             backref=db.backref('ride', lazy='dynamic'))
    passenger_id = db.Column(db.String(255), db.ForeignKey('passenger_info.passenger_id'))
    passenger = db.relationship('Passenger',
                                backref=db.backref('ride', lazy='dynamic'))
    request_id = db.Column(db.Integer, db.ForeignKey('request_info.id'))
    request = db.relationship('Request',
                              backref=db.backref('ride', lazy='dynamic'))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    status = db.Column(db.String(30), default=RIDE_NO_ACCEPTED)
    fare_estimate = db.Column(db.Float)

    def __init__(self, driver, request):
        self.driver = driver
        self.passenger = request.passenger
        self.request = request
        self.fare_estimate = MathHelper.calculate_estimate(request)

    def __repr__(self):
        return "<Ride: [Driver: {} Passenger: {} Status: {} Created On: {}]>".format(
            self.driver, self.passenger, self.status, self.created_on
        )

    @classmethod
    def get_ride_by_driver(driver):
        return Ride.query.filter_by(driver_id=driver.driver_id).first()

    @staticmethod
    def get_by_id(id):
        return Ride.query.fitler_by(id=id).first()

    def update_status(self, status):
        self.status = status
        db.session.commit()
        return self

    class InvalidStatus(Exception): pass


class CompletedRides(BaseModel, db.Model):
    __tablename__ = 'completed_ride'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ride_id = db.Column(db.Integer, db.ForeignKey(Ride.__tablename__ + ".id"))
    ride = db.relationship(Ride.__name__,
                           backref=db.backref(__tablename__, lazy='dynamic'))
    completed_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, ride):
        self.ride = ride

    def __repr__(self):
        return "<Ride: {} Completed on: {}>".format(self.ride, self.completed_on)


class CancelledRides(BaseModel, db.Model):
    __tablename__ = 'cancelled_ride'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ride_id = db.Column(db.Integer, db.ForeignKey(Ride.__tablename__ + ".id"))
    ride = db.relationship(Ride.__name__,
                           backref=db.backref(__tablename__, lazy='dynamic'))
    cancelled_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, ride):
        self.ride = ride

    def __repr__(self):
        return "<Ride: {} Cancelled on: {}>".format(self.ride, self.cancelled_on)
