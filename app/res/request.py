import json

from flask import Blueprint, Response
from flask_restful import Resource, Api, reqparse

import config
from app.auth.auth import auth
from app.models.request import Request

JSON_TYPE = 'application/json'
NOT_FOUND_MSG = '{"message": "The requested record was not found.", "status": "ERROR"}'
OK_MSG = '{"message": "OK"}'

class RequestsRes(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument(
			'origin_lat',
			type=float,
			required=True,
			help="Origin latitude was not provided"
		)
		self.parser.add_argument(
			'origin_lng',
			type=float,
			required=True,
			help="Origin longitude was not provided"
		)
		self.parser.add_argument(
			'destination_lat',
			type=float,
			required=True,
			help="Destination latitude was not provided"
		)
		self.parser.add_argument(
			'destination_lng',
			type=float,
			required=True,
			help="Origin longitude was not provided"
		)
		self.parser.add_argument(
			'number_of_passenger',
			type=int,
			required=True,
			help="Number of passenger was not provided"
		)

		self.REQUEST_NOT_FOUND = Response(NOT_FOUND_MSG, 
			status=404, mimetype=JSON_TYPE)
		super().__init__()

	@auth.login_required
	def get(self, id):
		request = Request.get_by_id(id)
		if request is None:
			return self.REQUEST_NOT_FOUND
		else:
			json_resp = json.dumps(
				{'data':
					{ Request.__tablename__: request.get_dict() }
				},
			indent=4)
			resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
			return resp

	@auth.login_required
	def put(self, id):
		request = Request.get_by_id(id)
		if request is None:
			return self.REQUEST_NOT_FOUND
		else:
			args = self.parser.parse_args()
			request.update(**args)
			json_resp = json.dumps(
				{'data':
					{ Request.__tablename__: request.get_dict() }
				},
			indent=4)
			resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
			return resp

	@auth.login_required
	def delete(self, id):
		request = Request.get_by_id(id)
		if request is None:
			return self.REQUEST_NOT_FOUND
		else:
			request.delete()
			return Response(OK_MSG, status=200, mimetype=JSON_TYPE)


class RequestsListRes(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument(
			'passenger_id',
			type=str,
			required=True,
			help="Passenger ID was not provided"
		)
		self.parser.add_argument(
			'origin_lat',
			type=float,
			required=True,
			help="Origin latitude was not provided"
		)
		self.parser.add_argument(
			'origin_lng',
			type=float,
			required=True,
			help="Origin longitude was not provided"
		)
		self.parser.add_argument(
			'destination_lat',
			type=float,
			required=True,
			help="Destination latitude was not provided"
		)
		self.parser.add_argument(
			'destination_lng',
			type=float,
			required=True,
			help="Origin longitude was not provided"
		)
		self.parser.add_argument(
			'number_of_passenger',
			type=int,
			required=True,
			help="Number of passenger was not provided"
		)

	def post(self):
		args = self.parser.parse_args()
		

request_api = Blueprint('app.res.request', __name__)

api = Api(request_api)

api.add_resource(
	RequestsRes,
	'/requests/<int:id>'
)

api.add_resource(
	RequestsListRes,
	'/requests'
)
