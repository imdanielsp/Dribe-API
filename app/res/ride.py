from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, url_for

from app.core.core import RideHandler
from app.models.ride import Ride, CompletedRides, CancelledRides


class RideRes(Resource):
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument(
			'id',
			type=str,
			help="Ride ID was not provided.",
			required=True
		)
		self.parser.add_argument(
			'values',
			type=str,
			help='Invalid values.'
		)
		super().__init__()

	def get(self):
		args = self.parser.parse_args()
		ride_id = args['id']
		
		if args['values']:
			values = args['values']
			print(values)

		return "Test"


ride_api = Blueprint('app.res.ride', __name__)

api = Api(ride_api)
api.add_resource(
	RideRes,
	'/rides',
	endpoint='ride'
)
