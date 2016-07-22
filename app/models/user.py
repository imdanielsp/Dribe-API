import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
					 	  BadSignature, SignatureExpired)

import config
from app.models.base import db, BaseModel
from app.core.tools import ModelHelper


class User(BaseModel, db.Model):
	__tablename__ = "user_info"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255), nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	date_joined = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, first_name, last_name, username, password):
		self.first_name = first_name
		self.last_name = last_name
		self.username = username
		self.password = ModelHelper.hash_password(password)

	def __repr__(self):
		return "<User: %s>" % self.username

	@staticmethod
	def verify_auth_token(token):
		serilizer = Serializer(config.SECRET_KEY)
		try:
			data = serilizer.loads(token)
		except (BadSignature, SignatureExpired):
			return None
		else:
			user = User.query.filter_by(id=data['id']).first()
			return user

	def verify_password(self, password):
		return ModelHelper.check_hash(password, self.password)

	def generate_auth_token(self, expires=36000):
		serilizer = Serializer(config.SECRET_KEY, expires_in=expires)
		return serilizer.dumps({'id': self.id})

	@staticmethod
	def get_user(username):
		return User.query.filter_by(username=username).first()
