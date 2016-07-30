import json

from flask import Blueprint, jsonify, Response
from flask_restful import Resource, Api, reqparse, url_for

from .base import *
from app.core.core import RideHandler
from app.models.ride import Ride, CompletedRides, CancelledRides

JSON_TYPE = 'application/json'


class RideRes(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument(
			'status',
			type=str,
			required=True,
			help="Status was not provided",
			location='args'
		)
		super().__init__()

	def get(self, ride_id):
		ride = Ride.get_by_id(ride_id)
		if ride is None:
			return get_not_found_response()
		else:	
			ride_info = ride.get_dict()
			json_resp = json.dumps(
				{'data':
					{ Ride.__tablename__: ride_info }
				},
			indent=4)
			resp = Response(json_resp, status=200, mimetype=JSON_TYPE)
			return resp

	def put(self, ride_id):
		ride = Ride.get_by_id(ride_id)
		if ride is None:
			return get_not_found_response()
		else:
			args = self.parser.parse_args()
			status = args.get('status')
			try:
				RideHandler.update_ride_status(ride, status)
			except Ride.InvalidStatus as e:
				msg = GENERIC_MSG % str(e)
				return Response(msg, status=400, mimetype=JSON_TYPE)
			else:
				msg = GENERIC_MSG % ("Status changed to %s" % status)
				resp = Response(msg, status=200, mimetype=JSON_TYPE)
				return resp


class RideStatusRes(Resource):
	def __init__(self):
		super().__init__()

	def get(self):
		json_resp = json.dumps({'ride_status': Ride.RIDE_STATUS_LIST})
		return Response(json_resp, status=200, mimetype=JSON_TYPE)


ride_api = Blueprint('app.res.ride', __name__)

api = Api(ride_api)
api.add_resource(
	RideRes,
	'/rides/<int:ride_id>',
	endpoint='ride'
)
api.add_resource(
	RideStatusRes,
	'/rides/status',
	endpoint='ride_status'
)
