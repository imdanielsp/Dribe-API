import datetime
import random

from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.request import Request
from app.models.tools import ModelHelper


class TestModelFactory:
    @staticmethod
    def get_driver():
        return Driver(
            "John", "Smith",
            datetime.datetime.now(),
            "%s@dribe.com" % ModelHelper.get_unique_id(),
            "password",
            "NapCorps"
        )

    @staticmethod
    def get_passenger():
        return Passenger(
            "Steve", "Jobs",
            datetime.datetime.now(),
            "steve%s@dribe.com" % ModelHelper.get_unique_id(),
            "Testing01234",
            str(int(random.random()*10000000000))  # Generate a random phone number
        )

    @staticmethod
    def get_request(passenger):
        return Request(
            passenger,
            42.707035,
            -71.163114
        )
