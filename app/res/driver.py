import json

from flask import Blueprint, Response, request, jsonify
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                           inputs)

from app.models.driver import Driver, DriversPool
from app.auth.auth import auth


JSON_TYPE = 'application/json'
NOT_FOUND_MSG = '{"message": "The requested record was not found.", "status": "ERROR"}'
OK_MSG = '{"message": "OK"}'

driver_fields = {
    'id': fields.Integer,
    'driver_id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'date_of_birth': fields.String,
    'address': fields.String,
    'email': fields.String,
    'phone_number': fields.String,
    'date_joined': fields.String,
    'company': fields.String
}

class DriverParser:
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'first_name',
            type=str,
            help="First name was not provided",
            required=True
        )
        self.parser.add_argument(
            'last_name',
            type=str,
            help="Last name was not provided",
            required=True
        )
        self.parser.add_argument(
            'date_of_birth',
            type=inputs.date,
            help="Date of birth was not provided",
            required=True
        )
        self.parser.add_argument(
            'address',
            type=str,
            help="Address was not provided",
            required=True
        )
        self.parser.add_argument(
            'email',
            type=str,
            help="Email was not provided",
            required=True
        )
        self.parser.add_argument(
            'password',
            type=str,
            help="Password was not provided",
            required=True
        )
        self.parser.add_argument(
            'phone_number',
            type=str,
            help="Phone number was not provided",
            required=True
        )
        self.parser.add_argument(
            'company',
            type=str,
            help="Company name was not provided",
            required=True
        )

    def build(self):
        return self.parser


class DriversRes(Resource):
    def __init__(self):
        self.parser = DriverParser().build()
        super().__init__()

    @auth.login_required
    def get(self, driver_id):
        driver = Driver.get_driver_by_id(driver_id)
        if driver is None:
            return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
            
        driver_info = marshal(driver.get_dict(), driver_fields)
        json_resp = json.dumps(
            {'data': 
                { Driver.__tablename__: driver_info}
            },
        indent=4)
        resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
        return resp

    @auth.login_required
    def put(self, driver_id):
        args = self.parser.parse_args()
        driver = Driver.get_driver_by_id(driver_id)
        if driver is None:
            return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
        else:
            driver.update(**args)
            json_resp = json.dumps({'data': marshal(driver.get_dict(), driver_fields)})
            resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
            return resp

    @auth.login_required
    def delete(self, driver_id):
        driver = Driver.get_driver_by_id(driver_id)
        if driver is None:
            return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
        else:
            driver.delete()
            return Response(OK_MSG, status=200, mimetype=JSON_TYPE)


class DriversListRes(Resource):
    def __init__(self):
        self.parser = DriverParser().build()
        super().__init__()

    @auth.login_required    
    def get(self):
        drivers = Driver.get_all()
        driver_list = [marshal(driver, driver_fields) for driver in drivers]
        json_resp = json.dumps({'data': driver_list})
        resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
        return resp

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        driver = Driver.build_from_args(**args)
        json_resp = json.dumps({'data': marshal(driver, driver_fields)})
        resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
        return resp


driver_api = Blueprint('app.res.driver', __name__)

api = Api(driver_api)
api.add_resource(
    DriversRes,
    '/drivers/<string:driver_id>'
)

api.add_resource(
    DriversListRes,
    '/drivers',
)
