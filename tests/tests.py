import os
import unittest

from tools import ModelFactory
from app.core.core import RideHandler, DriverHandler
from app.models.ride import Ride
from app.models.driver import DriversPool


class TestRideHandler(unittest.TestCase):
	"""
	Unittest for the RideHandler
	"""
	def setUp(self):
		self.driver = ModelFactory.get_driver().create()
		self.driver_pool = ModelFactory.make_driver_online(self.driver)
		self.passenger = ModelFactory.get_passenger().create()
		self.request = ModelFactory.get_request(self.passenger).create()
		self.crazy_request = ModelFactory.get_crazy_request(self.passenger).create()
		self.ride = RideHandler.create_ride(self.request, False)
		self.q0 = RideHandler.push_request(self.request)
		self.r1 = ModelFactory.get_request(self.passenger).create()
		self.q1 = RideHandler.push_request(self.r1)
		self.r2 = ModelFactory.get_request(self.passenger).create()
		self.q2 = RideHandler.push_request(self.r2)
		self.r3 = ModelFactory.get_request(self.passenger).create()
		self.q3 = RideHandler.push_request(self.r3)
		self.r4 = ModelFactory.get_request(self.passenger).create()
		self.q4 = RideHandler.push_request(self.r4)

	def tearDown(self):
		self.q0.delete()
		self.q1.delete()
		self.r1.delete()
		self.q2.delete()
		self.r2.delete()
		self.q3.delete()
		self.r3.delete()
		self.q4.delete()
		self.r4.delete()
		self.ride.delete()
		self.request.delete()
		self.crazy_request.delete()
		self.passenger.delete()
		self.driver_pool.delete()
		self.driver.delete()

	def test_push_request(self):
		queued_ride = RideHandler.push_request(self.request)
		self.assertEqual(self.request, RideHandler.get_front_request().request)
		queued_ride.delete()

	def test_get_front_request(self):
		self.assertEqual(self.request, RideHandler.get_front_request().request)

	def test_get_closer_driver(self):
		drivers = DriversPool.get_available_driver(self.request)
		driver = RideHandler._get_closer_driver(self.request, drivers)
		
		self.assertIsNotNone(driver)

	def test_get_driver_for_ride_no_available(self):
		with self.assertRaises(RideHandler.NoDriversAvailable):
			RideHandler._get_driver_for_ride(self.crazy_request)

	def test_get_driver_for_ride(self):
		driver = RideHandler._get_driver_for_ride(self.request)
		self.assertIsNotNone(driver)

	def test_create_ride(self):
		ride = RideHandler.create_ride(self.request, delete_request=False)
		
		self.assertIsNotNone(ride)
		on_db_ride = Ride.query.filter_by(id=ride.id).first()
		self.assertEqual(on_db_ride.status, Ride.RIDE_NO_ACCEPTED)

		on_db_ride.delete()

	def test_update_ride_status(self):
		current_passengers = DriversPool.get_by_driver(self.ride.driver).current_passengers
		self.assertEqual(current_passengers, 0)

		RideHandler.update_ride_status(self.ride, Ride.RIDE_PROCESSING)
		self.assertEqual(self.ride.status, Ride.RIDE_PROCESSING)

		RideHandler.update_ride_status(self.ride, Ride.RIDE_ACTIVE)
		self.assertEqual(self.ride.status, Ride.RIDE_ACTIVE)
		self.assertEqual(current_passengers + self.request.number_of_passenger, 2)

		driver_pool = RideHandler.update_ride_status(self.ride, Ride.RIDE_COMPLETED)
		self.assertEqual(self.ride.status, Ride.RIDE_COMPLETED)		
		self.assertEqual(driver_pool.current_passengers, 0)

		RideHandler.update_ride_status(self.ride, Ride.RIDE_CANCELED)
		self.assertEqual(self.ride.status, Ride.RIDE_CANCELED)

	def test_invalid_status(self):
		with self.assertRaises(Ride.InvalidStatus):
			RideHandler.update_ride_status(self.ride, "This is an invalid status")

			
if __name__ == '__main__':
	unittest.main()
