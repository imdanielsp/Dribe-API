import time
from operator import itemgetter

from app.core.tools import MathHelper
from app.models.driver import DriversPool
from app.models.request import RequestQueue
from app.models.ride import Ride, CompletedRides, CancelledRides


class RideHandler:
    @staticmethod
    def create_ride(request, delete_request=True):
        """
        This function creates a ride from a given request.
        If drivers are no available returns None, otherwise
        returns a Ride.
        :param delete_request:
        :param request:
        """
        driver = RideHandler._get_driver_for_ride(request)
        ride = Ride(request, request.passenger, driver).create()

        if delete_request:
            RequestQueue.get_by_request(request).delete()
        return ride

    @staticmethod
    def get_driver_rides(driver):
        return Ride.get_ride_by_driver(driver)

    @staticmethod
    def update_ride_status(ride, status):
        driver_pool = DriversPool.get_by_driver(ride.driver)
        if status == Ride.RIDE_COMPLETED:
            CompletedRides(ride).create()
            driver_pool.update_current_capacity(-ride.request.number_of_passenger)
        elif status == Ride.RIDE_CANCELED:
            CancelledRides(ride).create()
        elif status == Ride.RIDE_ACTIVE:
            driver_pool.update_current_capacity(ride.request.number_of_passenger)
        elif status == Ride.RIDE_PROCESSING:
            pass
        else:
            error_msg = "{} is an invalid status".format(status)
            raise Ride.InvalidStatus(error_msg)
        ride.update_status(status)
        return driver_pool

    @staticmethod
    def _get_driver_for_ride(request):
        driver_in_pool = DriversPool.get_available_driver(request)
        if driver_in_pool:
            return RideHandler._get_closer_driver(request, driver_in_pool)
        else:
            raise RideHandler.NoDriversAvailable("No drivers available at this moment")

    @staticmethod
    def _get_closer_driver(request, drivers):
        distance_list = []
        for driver in drivers:
            distance_list.append(MathHelper.get_distance(driver, request))
        # This will sort the list of (Driver, distance) base on the distance
        distance_list.sort(key=itemgetter("distance"))
        # Here we get the first item of the sorted list and return the driver
        # in the dictionary
        return distance_list[0]["driver"]

    class NoDriversAvailable(Exception):
        pass


class DriverHandler:
    @staticmethod
    def _put_driver_in_pool(driver, capacity, latitude, longitude):
        driver_pool = DriversPool(driver, capacity, latitude, longitude).create()
        return driver_pool

    @staticmethod
    def _remove_driver_from_pool(driver):
        DriversPool.get_by_driver(driver).delete()

    make_driver_online = _put_driver_in_pool
    make_driver_offline = _remove_driver_from_pool


class RequestHandler:
    @staticmethod
    def get_front_request():
        return RequestQueue.get_first()

    @staticmethod
    def push_request(request):
        return RequestQueue(request).create()


class Application:
    @staticmethod
    def run():
        request_queue = RequestHandler.get_front_request()

        if request_queue:
            request = request_queue.request
            print("Request found!")
            print(request)
            print("Creating ride....")
            ride = RideHandler.create_ride(request)
            if ride:
                print("Ride created")
                print(ride)
            else:
                print("Couldn't create ride\nTrying again...")
        else:
            print("No request available")
        print("Sleeping...")
        time.sleep(2)
