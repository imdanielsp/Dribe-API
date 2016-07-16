import datetime

from app.models.base import db, BaseModel
from app.models.passenger import Passenger


class Request(BaseModel, db.Model):
    __tablename__ = 'request_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passenger_id = db.Column(db.String(255),
                             db.ForeignKey('passenger_info.passenger_id'))
    passenger = db.relationship(Passenger.__name__,
                                backref=db.backref(__tablename__, lazy='dynamic'))
    request_latitude = db.Column(db.Float, nullable=False)
    request_longitude = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, passenger, latitude, longitude):
        self.passenger = passenger
        self.request_latitude = latitude
        self.request_longitude = longitude

    def __repr__(self):
        return "<Request By: {} on {} - Lat: {} Long: {}>".format(
            self.passenger.get_full_name(),
            self.created_on, self.request_latitude,
            self.request_longitude
        )


class RequestQueue(BaseModel, db.Model):
    __tablename__ = 'request_queue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request_info.id'))
    request = db.relationship(Request.__name__,
                              backref=db.backref(__tablename__, lazy='dynamic'))
    added_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, request):
        self.request = request

    def __repr__(self):
        return "<In Request Queue: %s>" % self.request
