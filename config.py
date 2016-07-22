import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
API_VERSION = '1'
URL_PREFIX = "/dribe/api/v{}".format(API_VERSION)
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

SECRET_KEY = "\x97C,e\xa4\xde'~\x96;?\xa2s\x88u\x8c\xbc\x00\xf6g\xdf\xa29\xcb"

DATABASE_CONFIG = {
    "DB_NAME": "dribe",
    "USERNAME": "root",
    "PASSWORD": "root",
    "LOCATION": "127.0.0.1",
    "PORT": "3306"
}
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USERNAME}:{PASSWORD}@{LOCATION}:{PORT}/{DB_NAME}".format(**DATABASE_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = True

RESET_DB = False

GOOGLE_API_KEY = "AIzaSyD-t8oUqqOg7uWTqV6n7zSBmyNluRQyPew"


def reset_system(db):
	if RESET_DB:
		db.drop_all()
		db.create_all()
		distance_rate = {
			"price": 2.5,
			"distance": 1
		}
		time_rate = {
			"price": 0.50,
			"time": 1
		}
		base_rate = 2.50
		peak_surcharge = 1.0
		from app.models.settings import Settings
		from app.models.user import User
		Settings("Liberty", base_rate, distance_rate, time_rate, peak_surcharge).create()
		User("Daniel", "Santos", "dsantosp12", "dribe1234").create()
	else:
		db.create_all()
