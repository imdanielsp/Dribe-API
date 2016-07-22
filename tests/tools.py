import datetime
import random

import faker

from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.request import Request
from app.core.tools import ModelHelper
from app.core.core import DriverHandler

fake = faker.Factory().create()


class ModelFactory:
    @staticmethod
    def get_driver():
        profile = fake.profile()
        return Driver(
            fake.first_name_male(),
            fake.last_name(),
            fake.date(),
            fake.address(),
            fake.profile()['mail'],
            fake.password(),
            fake.phone_number(),
            fake.company()
        )

    @staticmethod
    def get_passenger():
        return Passenger(
            fake.first_name_male(),
            fake.last_name_male(),
            fake.date(),
            fake.profile()['mail'],
            fake.password(),
            fake.phone_number()
        )

    @staticmethod
    def get_request(passenger):
        return Request(
            passenger,
            42.656755,
            -71.142124,
            42.701898,
            -71.147712,
            2
        )

    @staticmethod
    def get_crazy_request(passenger):
        return Request(
            passenger,
            42.656755,
            -71.142124,
            42.701898,
            -71.147712,
            20
        )        

    @staticmethod
    def make_driver_online(driver):
        return DriverHandler.make_driver_online(
            driver, 4, 42.698645, -71.157182
        )

