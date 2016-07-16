from flask import Blueprint, jsonify
from flask_restful import (Resource, Api, reqparse, fields, marshal_with,
                           url_for)
import sqlalchemy.exc as alchemy_exceptions

from app.models.driver import Driver
from app.models.tools import ModelHelper

driver_fields = {
    'driver_api_id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'date_of_birth': fields.DateTime("iso8601"),
    'email': fields.String,
    'date_joined': fields.DateTime("iso8601"),
    'company': fields.String
}


def driver_or_404(driver_id):
    return Driver.query.filter_by(driver_api_id=driver_id).first_or_404()


class DriverRes(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'first_name',
            required=True,
            help='First name was not provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'last_name',
            required=True,
            help='Last name was not provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'date_of_birth',
            required=True,
            help='Date of birth was not provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='Email was not provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help="Password was not provided",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'company',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(driver_fields)
    def get(self, driver_id):
        return driver_or_404(driver_id)

    @marshal_with(driver_fields)
    def post(self):
        args = self.reqparse.parse_args()
        try:
            driver = Driver.build_from_arg(**args).create()
        except alchemy_exceptions.IntegrityError:
            return jsonify(messeage='Duplicate email')
        else:
            return (driver, 201, {
                'Location': url_for('app.res.driver.driver', driver_id=driver.driver_api_id)
            })


class DriverSessionHelper(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'hash',
            required=True,
            help='No hash provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        return jsonify(auth=ModelHelper.check_hash(args['password'],
                                                   args['hash']))


driver_api = Blueprint('app.res.driver', __name__)
driver_session_helper_api = Blueprint('app.res.driver.auth', __name__)

api = Api(driver_api)
api.add_resource(
    DriverRes,
    '/driver',
    '/driver/<string:driver_id>',
    endpoint='driver'
)
api.add_resource(
    DriverSessionHelper,
    '/driver/auth',
    endpoint='driver_session_helper'
)
