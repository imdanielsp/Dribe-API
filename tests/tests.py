import os
import unittest
import json

import requests

import config
from tools import ModelFactory
from app.core.core import RideHandler, DriverHandler
from app.core.tools import ModelHelper
from app.models.ride import Ride
from app.models.driver import Driver, DriversPool

AUTH = config.AUTH


class TestDriverModel(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_update_complete_info(self):
		pass

	def test_update_missing_info(self):
		pass

	def test_get_driver_by_id_correct(self):
		pass

	def test_get_driver_by_id_fake(self):
		pass

	def test_build_from_args_complete(self):
		pass

	def test_build_from_args_incomplete(self):
		pass


class TestDriversPoolModel(unittest.TestCase):
	def test_get_coordinates(self):
		pass

	def test_get_available_driver(self):
		pass

	def test_get_driver_by_id_correct(self):
		pass

	def test_get_driver_by_id_fake(self):
		pass

	def test_get_by_id_correct(self):
		pass

	def test_get_by_id_fake(self):
		pass

	def test_get_by_driver_correct(self):
		pass

	def test_get_by_driver_fake(self):
		pass

	def test_build_from_args_complete(self):
		pass

	def test_build_from_args_incomplete(self):
		pass

	def test_update_current_capacity(self):
		pass

	def test_update_current_capacity_with_number_greater_capacity(self):
		pass


class TestRequestQueue(unittest.TestCase):
	def test_get_first(self):
		pass

	def test_get_by_request(self):
		pass


class TestPassengerModel(unittest.TestCase):
	def test_update

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


class TestDriverResource(unittest.TestCase):
	def setUp(self):
		self.get = requests.get
		self.post = requests.post
		self.put = requests.put
		self.delete = requests.delete
		self.driver = ModelFactory.get_driver().create()
		self.base_url = "http://{HOST}:{PORT}{URL_PREFIX}/drivers".format(
			HOST=config.HOST, 
			PORT=config.PORT, 
			URL_PREFIX=config.URL_PREFIX
		)
		self.url = self.base_url + "/{DRIVER_ID}".format(
			DRIVER_ID=self.driver.driver_id
		)

	def tearDown(self):
		self.driver.delete()

	def test_drivers_get(self):
		wrong_url = self.base_url + "/kdsfas9401234"
		response = self.get(self.url, auth=AUTH)
		data = response.json()

		self.assertEqual(response.status_code, 200)

		driver_id = data['data']['driver_info']['driver_id']

		self.assertEqual(driver_id, self.driver.driver_id)

		response = self.get(wrong_url, auth=AUTH)
		data = response.json()

		self.assertEqual(response.status_code, 404)
		self.assertEqual(data['status'], "ERROR")

	def test_drivers_post(self):
		# driver = ModelFactory.get_driver()
		# response = self.post(self.base_url, auth=AUTH, data=driver.get_dict())

		# self.assertEqual(response.status_code, 201)

		# driver.delete()
		pass

	def test_drivers_put(self):
		new_email = "test_email@dribe.com"
		new_phone_number = "999-123-2345"
		new_address = "123 Main St \nBoston, MA 01943"
		new_password = "Password1234"
		driver_info = self.driver.get_dict()
		driver_info.pop('id')
		driver_info.pop('date_joined')
		driver_info['email'] = new_email
		driver_info['password'] = new_password
		driver_info['phone_number'] = new_phone_number
		driver_info['address'] = new_address
		response = self.put(self.url, auth=AUTH, data=driver_info)
	
		self.assertEqual(response.status_code, 200)
		
		new_driver = response.json()['data'][Driver.__tablename__]

		self.assertEqual(new_driver['email'], new_email)
		self.assertEqual(new_driver['phone_number'], new_phone_number)
		self.assertEqual(new_driver['address'], new_address)
		#  Need to test for the new password

	def test_drivers_delete(self):
		del_response = self.delete(self.url, auth=AUTH)
		get_response = self.get(self.url, auth=AUTH)

		self.assertEqual(del_response.status_code, 200)
		self.assertEqual(del_response.json()['message'], "OK")
		self.assertEqual(get_response.status_code, 404)
		self.assertEqual(get_response.json()['status'], "ERROR")


class TestDriverPoolResource(unittest.TestCase):
	def setUp(self):
		self.base_url = "http://{HOST}:{PORT}{URL_PREFIX}/drivers/driverspools".format(
			HOST=config.HOST, 
			PORT=config.PORT, 
			URL_PREFIX=config.URL_PREFIX
		)
		self.driver = ModelFactory.get_driver().create()
		self.post = requests.post
		self.get = requests.get
		self.delete = requests.delete
		self.data = {
		    "driver_id": self.driver.driver_id,
		    "capacity": 6,
		    "current_psgr": 0,
		    "lat": 41.0984,
		    "lng": -71.98432
		}

	def tearDown(self):
		self.driver.delete()

	def test_drivers_pools_get(self):
		url = self.base_url + "/" + self.driver.driver_id
		response = self.get(url, auth=AUTH)
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['status'], "OFFLINE")

		response = self.post(self.base_url, auth=AUTH, data=self.data)
		self.assertEqual(response.status_code, 201)

		response = self.get(url, auth=AUTH)
		self.assertEqual(response.json()['status'], "ONLINE")

		url = "/" + self.driver.driver_id	
		self.delete(self.base_url + url, auth=AUTH)

	def test_driver_make_online(self):
		response = self.post(self.base_url, data=self.data, auth=AUTH)

		self.assertEqual(response.status_code, 201)
		
		url = self.base_url + "/" + self.driver.driver_id
		response = self.get(url, auth=AUTH)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['status'], "ONLINE")

		url = "/" + self.driver.driver_id	
		self.delete(self.base_url + url, auth=AUTH)

	def test_driver_make_offline(self):
		response = self.post(self.base_url, data=self.data, auth=AUTH)

		self.assertEqual(response.status_code, 201)

		url = self.base_url + "/" + self.driver.driver_id
		response = self.delete(url, auth=AUTH)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['message'], "OK")

		response = self.get(url, auth=AUTH)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()['status'], "OFFLINE")


class TestDriverPoolsUpdateResource(unittest.TestCase):
	def setUp(self):
		self.driver = ModelFactory.get_driver().create()
		self.drv_pool = ModelFactory.make_driver_online(self.driver)
		self.base_url = "http://{HOST}:{PORT}{URL_PREFIX}/drivers/driverspools".format(
			URL_PREFIX=config.URL_PREFIX, HOST=config.HOST, PORT=config.PORT	
		)
		self.put = requests.put
		self.get = requests.get

	def tearDown(self):
		ModelFactory.make_driver_offline(self.driver)
		self.driver.delete()

	def test_put_update_driver_pool_location(self):		
		new_lat = 12.34
		new_lng = 89.012
		data = {
			'lat': new_lat,
			'lng': new_lng
		}
		url = self.base_url + "/" + self.driver.driver_id
		resp = self.put(url, data=data, auth=AUTH)
	
		self.assertEqual(resp.status_code, 200)
		
		resp = self.get(url, auth=AUTH)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json()['lat'], new_lat)
		self.assertEqual(resp.json()['lng'], new_lng)	
		

if __name__ == '__main__':
	unittest.main()
