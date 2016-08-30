import datetime
import random

import faker

from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.request import Request
from app.models.ride import Ride
from app.core.tools import ModelHelper
from app.core.core import DriverHandler, RequestHandler

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
    def make_request(passenger, origin_lat, origin_lng, 
        dest_lat, dest_lng, num_passenger):
        return Request(passenger, origin_lat, origin_lng, 
            dest_lat, dest_lng, num_passenger)

    @staticmethod
    def get_request(passenger):
        return ModelFactory.make_request(passenger, 
            42.656755, -71.142124, 
            42.701898, -71.147712, 
            2
        )

    @staticmethod
    def get_crazy_request(passenger):
        return make_request(
            passenger,
            42.656755,
            -71.142124,
            42.701898,
            -71.147712,
            20
        )        

    @staticmethod
    def create_driver_pool(driver, capacity, lat, lng):
        return DriverHandler.make_driver_online(
            driver, capacity, lat, lng
        )

    @staticmethod
    def make_driver_online(driver):
        return DriverHandler.create_driver_pool(
            driver, 4, 42.698645, -71.157182
        )

    @staticmethod
    def make_driver_offline(driver):
        return DriverHandler.make_driver_offline(driver)

    @staticmethod
    def create_ride(request, passenger, driver):
        return Ride(request, passenger, driver)

    @staticmethod
    def make_scenario(number):
        if number == 1:
            psgr1 = ModelFactory.get_passenger().create()
            psgr2 = ModelFactory.get_passenger().create()
            psgr3 = ModelFactory.get_passenger().create()
            psgr4 = ModelFactory.get_passenger().create()

            drv1 = ModelFactory.get_driver().create()
            drv2 = ModelFactory.get_driver().create()
            drv3 = ModelFactory.get_driver().create()
            drv4 = ModelFactory.get_driver().create()

            drv_pool1 = ModelFactory.create_driver_pool(drv1, 4, 42.697006, -71.158436).create()
            drv_pool2 = ModelFactory.create_driver_pool(drv2, 4, 42.709288, -71.181895).create()
            drv_pool3 = ModelFactory.create_driver_pool(drv3, 4, 42.682128, -71.161262).create()
            drv_pool4 = ModelFactory.create_driver_pool(drv4, 4, 42.688209, -71.154157).create()

            req1 = ModelFactory.make_request(
                psgr1, 42.709868, -71.167124, 
                42.694107, -71.150497, 2)

            req2 = ModelFactory.make_request(
                psgr2, 42.704693, -71.184449, 
                42.717371, -71.165685, 3)

            req3 = ModelFactory.make_request(
                psgr3, 42.709546, -71.144066, 
                42.702240, -71.155421, 1)

            req4 = ModelFactory.make_request(
                psgr4, 42.690594, -71.167867,
                42.692291, -71.146247, 2
            )

            #  rq = Request Queue
            rq1 = RequestHandler.push_request(req1)
            rq2 = RequestHandler.push_request(req2)
            rq3 = RequestHandler.push_request(req3)
            rq4 = RequestHandler.push_request(req4)

            return [
                rq1, rq2, rq3, rq4,
                req1, req2, req3, req4, 
                drv_pool1, drv_pool2, drv_pool3, drv_pool4, 
                drv1, drv2, drv3, drv4,
                psgr1, psgr2, psgr3, psgr4
            ]








