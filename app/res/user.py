from flask import Blueprint, jsonify, g
from flask_restful import Resource, Api

from app.auth.auth import auth


class UserRes(Resource):
    def __init__(self):
        super().__init__()

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})


user_api = Blueprint('app.res.user', __name__)

api = Api(user_api)
api.add_resource(
    UserRes,
    '/user/token',
    endpoint='user_token'
)
