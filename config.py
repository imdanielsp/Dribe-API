import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
URL_PREFIX = "/api/v1"
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
