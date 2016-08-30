import datetime

from app.models.base import db, BaseModel, LAZY
from app.models.passenger import Passenger


class Request(BaseModel, db.Model):
    __tablename__ = 'request_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passenger_id = db.Column(
        db.String(255),
        db.ForeignKey(Passenger.__tablename__ + '.passenger_id'),
        nullable=False
    )
    passenger = db.relationship(Passenger.__name__,
                                backref=db.backref(__tablename__, lazy=LAZY))
    origin_latitude = db.Column(db.Float, nullable=False)
    origin_longitude = db.Column(db.Float, nullable=False)
    destination_latitude = db.Column(db.Float, nullable=False)
    destination_longitude = db.Column(db.Float, nullable=False)
    number_of_passenger = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, passenger, origin_latitude, origin_longitude,
                 dest_latitude, dest_longitude, number_of_passenger):
        self.passenger = passenger
        self.passenger_id = passenger.passenger_id
        self.origin_latitude = origin_latitude
        self.origin_longitude = origin_longitude
        self.destination_latitude = dest_latitude
        self.destination_longitude = dest_longitude
        self.number_of_passenger = number_of_passenger

    def __repr__(self):
        return "<Request By: {} on {}>".format(self.passenger.get_full_name(),
                                               self.created_on)

    #  Need to rename this to get_origin_coordinates
    #  post renaming, remove the deprecated decorator
    def get_coordinates(self):
        return self.origin_latitude, self.origin_latitude

    def update(self, **kwargs):
        self.origin_latitude = kwargs['origin_lat']
        self.origin_longitude = kwargs['origin_lng']
        self.destination_latitude = kwargs['destination_lat']
        self.destination_longitude = kwargs['destination_lng']
        self.number_of_passenger = kwargs['number_of_passenger']
        self.save()

    def get_destination_coordinates(self):
        return self.destination_latitude, self.destination_longtidue

    def get_dict(self):
        return {
            'passenger_id': self.passenger_id,
            'origin_lat': self.origin_latitude,
            'origin_lng': self.origin_longitude,
            'destination_lat': self.destination_latitude,
            'destination_lng': self.destination_longitude,
            'number_of_passenger': self.number_of_passenger,
            'created_on': self.created_on.__str__()
        }

    @staticmethod
    def build_from_args(**kwargs):
        passenger = Passenger.get_by_id(kwargs['passenger_id'])
        return Request(
            passenger,
            kwargs['origin_lat'],
            kwargs['origin_lng'],
            kwargs['destination_lat'],
            kwargs['destination_lng'],
            kwargs['number_of_passenger']
        ).create()

    @staticmethod
    def get_by_id(request_id):
        return Request.query.filter_by(id=request_id).first()


class RequestQueue(BaseModel, db.Model):
    __tablename__ = 'request_queue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request_info.id'))
    request = db.relationship(Request.__name__,
                              backref=db.backref(__tablename__, lazy=LAZY))
    added_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, request):
        self.request = request

    def __repr__(self):
        return "<In Request Queue: %s Id: %d>" % (self.request, self.id)

    @staticmethod
    def get_first():
        return RequestQueue.query.order_by(RequestQueue.added_on).first()

    @staticmethod
    def get_by_request(request):
        return RequestQueue.query.filter_by(request_id=request.id).first()
