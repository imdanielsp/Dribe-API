import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from app.res.driver import driver_api, driver_session_helper_api
from app.models.driver import Driver, DriversPool
from app.models.passenger import Passenger
from app.models.request import Request, RequestQueue
from app.models.ride import Ride, CompletedRides, CancelledRides

# API Registration
app.register_blueprint(driver_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(driver_session_helper_api, url_prefix=config.URL_PREFIX)


@app.route('/')
def index():
    from app.test.tools import TestModelFactory
    passenger = TestModelFactory.get_passenger().create()
    print(passenger)
    request = TestModelFactory.get_request(passenger).create()
    print(request)
    return "Hello world"
