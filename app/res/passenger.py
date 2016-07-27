import json

from flask import Blueprint, Response, jsonify
from flask_restful import (Resource, Api, reqparse, fields, 
							marshal, inputs)

from app.models.passenger import Passenger
from app.auth.auth import auth

JSON_TYPE = 'application/json'
NOT_FOUND_MSG = '{"message": "The requested record was not found.", "status": "ERROR"}'
OK_MSG = '{"message": "OK"}'

psgr_fields = {
	'id': fields.Integer,
	'passenger_id': fields.String,
	'first_name': fields.String,
	'last_name': fields.String,
	'date_of_birth': fields.String,
	'email': fields.String,
	'phone_number': fields.String,
	'date_joined': fields.String,	
	'is_active': fields.Boolean
}


class PassengerParser:
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

	def build(self):
		return self.parser


class PassengerRes(Resource):
	def __init__(self):
		self.parser = PassengerParser().build()
		super().__init__()

	@auth.login_required
	def get(self, passenger_id):
		psgr = Passenger.get_by_id(passenger_id)
		if psgr is None:
			return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
		else:
			psgr_info = marshal(psgr.get_dict(), psgr_fields)
			json_resp = json.dumps(
				{'data':
					{ Passenger.__tablename__: psgr_info }
				},
			indent=4)
			resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
			return resp

	@auth.login_required
	def put(self, passenger_id):
		args = self.parser.parse_args()
		psgr = Passenger.get_by_id(passenger_id)
		if psgr is None:
			return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
		else:
			psgr.update(**args)
			json_resp = json.dumps(
				{'data': 
					{ Passenger.__tablename__: marshal(psgr.get_dict(), psgr_fields)}
				},
			indent=4)
			resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
			return resp

	@auth.login_required
	def delete(self, passenger_id):
		psgr = Passenger.get_by_id(passenger_id)
		if psgr is None:
			return Response(NOT_FOUND_MSG, status=404, mimetype=JSON_TYPE)
		else:
			psgr.delete()
			return Response(OK_MSG, status=200, mimetype=JSON_TYPE)


class PassengerListRes(Resource):
	def __init__(self):
		self.parser = PassengerParser().build()
		super().__init__()

	@auth.login_required
	def get(self):
		psgrs = Passenger.get_all()
		psgr_list = [marshal(psgr, psgr_fields) for psgr in psgrs]
		json_resp = json.dumps({'data': psgr_list}, indent=4)
		resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
		return resp

	@auth.login_required
	def post(self):
		args = self.parser.parse_args()
		psgr = Passenger.build_from_args(args)
		json_resp = json.dumps(
			{'data': 
				{ Passenger.__tablename__: marshal(psgr, psgr_fields)}
			},
		indent=4)
		resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
		return resp


passenger_api = Blueprint('app.res.passenger', __name__)

api = Api(passenger_api)
api.add_resource(
	PassengerRes,
	'/passengers/<string:passenger_id>',
)
api.add_resource(
	PassengerListRes,
	'/passengers'
)
