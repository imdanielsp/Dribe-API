from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

from app.models.user import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')
auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    user = User.get_user(username)
    if user is None:
        return False
    else:
        if user.verify_password(password):
            g.user = user
            return True
    return False


@token_auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False
