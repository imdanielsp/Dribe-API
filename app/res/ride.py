from flask import Blueprint, jsonify, Response
from flask_restful import Resource, Api, reqparse, url_for

from app.core.core import RideHandler
from app.models.ride import Ride, CompletedRides, CancelledRides

JSON_TYPE = 'application/json'

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

	def get(self, ride_id):
		ride = Ride.get_by_id(ride_id)
		if ride is None:
			return 
		return ride_id


ride_api = Blueprint('app.res.ride', __name__)

api = Api(ride_api)
api.add_resource(
	RideRes,
	'/rides/<int:ride_id>',
	endpoint='ride'
)
