from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

import config
from app.tasks.tasks import make_celery

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
celery = make_celery(app)

#   API Resources Imports
from app.res.driver import driver_api
from app.res.user import user_api
from app.res.passenger import passenger_api
from app.res.request import request_api
from app.res.ride import ride_api

#   API Models Imports
from app.models.user import User
from app.models.driver import Driver, DriversPool
from app.models.passenger import Passenger
from app.models.request import Request, RequestQueue
from app.models.ride import Ride, CompletedRides, CancelledRides

#   API Tools Imports
from app.core.core import RideHandler, DriverHandler, Application
from app.google.matrix import MatrixApi
from app.core.tools import MathHelper

#   API Registration
app.register_blueprint(driver_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(user_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(passenger_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(request_api, url_prefix=config.URL_PREFIX)
app.register_blueprint(ride_api, url_prefix=config.URL_PREFIX)


@celery.task()
def run():
    Application.run()


@app.route('/run')
def start_app():
    run.apply_async()


@app.route('/make-scenario/<int:scenario>')
def create_scenario(scenario):
    from tests.tools import ModelFactory
    g.data = ModelFactory.make_scenario(scenario)
    if g.data:
        return "Scenario created"
    else:
        return "An error occurred"


@app.route('/delete-scenarios')
def delete_scenarios():
    if g.data:
        for obj in g.data:
            obj.delete()
        g.data = None
        return "Deleted"
    else:
        return "No scenarios created before"
