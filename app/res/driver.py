import json

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, Response
from flask_restful import (Resource, Api, reqparse, fields,
                           marshal, inputs)

from .base import *
from app.models.driver import Driver, DriversPool
from app.auth.auth import auth

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
        else:
            driver_info = marshal(driver.get_dict(), driver_fields)
            json_resp = json.dumps(
                {
                    'data':
                    {
                        Driver.__tablename__: driver_info
                    }
                }, indent=4)
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
            json_resp = json.dumps(
                {
                    'data':
                    {
                        Driver.__tablename__: marshal(driver.get_dict(), driver_fields)
                    }
                }, indent=4)
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
        json_resp = json.dumps(
            {
                'data':
                {
                    Driver.__tablename__: marshal(driver, driver_fields)
                }
            }, indent=4)
        resp = Response(json_resp, status=201, mimetype=JSON_TYPE)
        return resp


class DriverPoolRes(Resource):
    """
    This Resource is the driver pool,
    GET: return is driver is ONLINE or OFFLINE
    POST: make driver ONLINE
    DELETE: make a driver OFFLINE
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'driver_id',
            type=str,
            help="Driver ID was not provided",
            required=True
        )
        self.parser.add_argument(
            'capacity',
            type=inputs.positive,
            help="Capacity was not provided",
            required=True
        )
        self.parser.add_argument(
            'current_psgr',
            type=inputs.natural,
            help="Current passenger number was not provided",
            required=True
        )
        self.parser.add_argument(
            'lat',
            type=float,
            help="Latitude was not provided",
            required=True
        )
        self.parser.add_argument(
            'lng',
            type=float,
            help="Longitude was not provided",
            required=True
        )
        super().__init__()

    @auth.login_required
    def get(self, drv_id):
        """
        Return information about the driver's status, ONLINE or OFFLINE
        :param drv_id:
        """
        drv_pool = DriversPool.get_by_driver_id(drv_id)
        if drv_pool:
            resp_data = DRIVER_ONLINE % (drv_pool.latitude, drv_pool.longitude)
            return Response(resp_data, status=200, mimetype=JSON_TYPE)
        else:
            return Response(DRIVER_OFFLINE, status=200, mimetype=JSON_TYPE)

    @auth.login_required
    def post(self):
        """
        Make a driver online given information via HTTP json forms
        """
        args = self.parser.parse_args()
        try:
            drv_pool = DriversPool.build_from_args(**args).create()
        except IntegrityError:
            msg = json.dumps({'message': 'Driver is already online.'})
            resp = Response(msg, status=200, mimetype=JSON_TYPE)
            return resp
        else:
            json_resp = json.dumps({'data': drv_pool.get_dict()})
            resp = Response(json_resp, status=201, mimetype=JSON_TYPE)
            return resp

    @auth.login_required
    def delete(self, drv_id):
        """
        Make a driver offline given the passed ID.
        :param drv_id:
        """
        drv_pool = DriversPool.get_by_driver_id(drv_id)
        if drv_pool is None:
            return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
        else:
            drv_pool.delete()
            return Response(OK_MSG, status=200, mimetype=JSON_TYPE)


class DriverPoolsUpdateRes(Resource):
    """
    This resource update the driver's location.
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'lat',
            type=float,
            required=True,
            help="Latitude was not provided."
        )
        self.parser.add_argument(
            'lng',
            type=float,
            required=True,
            help="Longitude was not provided"
        )
        super().__init__()

    @auth.login_required
    def put(self, drv_id):
        """
        Update the driver's location
        """
        args = self.parser.parse_args()
        drv_pool = DriversPool.get_by_driver_id(drv_id)
        if drv_pool is None:
            return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
        else:
            drv_pool.latitude = args['lat']
            drv_pool.longitude = args['lng']
            drv_pool.save()
            return Response(OK_MSG, status=200, mimetype=JSON_TYPE)


driver_api = Blueprint('app.res.driver', __name__)

api = Api(driver_api)
api.add_resource(
    DriversRes,
    '/drivers/<string:driver_id>',
)

api.add_resource(
    DriversListRes,
    '/drivers',
)

api.add_resource(
    DriverPoolRes,
    '/drivers/driverspools',
    '/drivers/driverspools/<string:drv_id>'
)

api.add_resource(
    DriverPoolsUpdateRes,
    '/drivers/driverspools/<string:drv_id>'
)
