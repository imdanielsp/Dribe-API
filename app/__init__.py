from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

#   API Resources Imports
from app.res.driver import driver_api
from app.res.user import user_api
from app.res.passenger import passenger_api
from app.res.ride import ride_api

#   API Models Imports
from app.models.user import User
from app.models.driver import Driver, DriversPool
from app.models.passenger import Passenger
from app.models.request import Request, RequestQueue
from app.models.ride import Ride, CompletedRides, CancelledRides

#   API Tools Imports
from app.core.core import RideHandler, DriverHandler
from app.google.matrix import MatrixApi
from app.core.tools import MathHelper

#   API Registration
app.register_blueprint(driver_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(user_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(passenger_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(ride_api, url_prefix=config.URL_PREFIX)


@app.route('/')
def index():
    from tests.tools import ModelFactory
    return "Index"
