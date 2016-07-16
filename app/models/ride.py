import datetime

from app.models.base import db, BaseModel


class Ride(BaseModel, db.Model):
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
    status = db.Column(db.String(15), default=RIDE_PROCESSING)

    def __init__(self, driver, passenger, request):
        self.driver = driver
        self.passenger = passenger
        self.request = request

    def __repr__(self):
        return "<Ride: [Driver: {} Passenger: {} Status: {} Created On: {}]>".format(
            self.driver, self.passenger, self.status, self.created_on
        )


class CompletedRides(BaseModel, db.Model):
    __tablename__ = 'completed_ride'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ride_id = db.Column(db.Integer, db.ForeignKey(Ride.__tablename__ + ".id"))
    ride = db.relationship(Ride.__name__,
                           backref=db.backref(__tablename__, lazy='dynamic'))
    completed_on = db.Column(db.DateTime, nullable=False)

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
    cancelled_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, ride):
        self.ride = ride

    def __repr__(self):
        return "<Ride: {} Cancelled on: {}>".format(self.ride, self.cancelled_on)
