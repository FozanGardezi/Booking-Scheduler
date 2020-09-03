import json

from django.utils import timezone, dateformat
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework_api_key.models import APIKey
from django.urls import reverse
from rest_framework import status
from django.forms.models import model_to_dict

from .models import Booking
from location.models import Location
from .serializers import BookingSerializer
from .views import BookingViewSet

# TODO: Figure out a better location for this import 
from mysite.scheduler.scheduler_jobs import TurnlightOnTask, sendLockCode

client = APIClient()

success_case_data = {
			"slotKey" : "-wowweareteating",
			"bookingKey" : "-wowweareteating",
			"date" : "2020-07-15T00:00:00+05:00",
			"duration" : 1,
			"end" : "11pm",
			"location" : "Orchid Country Club",
			"name" : "Fozan Ali",
			"pitch" : 2,
			"rate" : 95,
			"start" : "10pm",
			"status" : "Paid",
			"sumittedDate" : "2020-02-27T13:17:09+08:00",
			"email": "ali.gardezi@tintash.com"
		}

failure_case_missing_data = {
			"slotKey" : "-wowweareteating",
			"bookingKey" : "-wowweareteating",
			"date" : "2020-07-08T00:00:00+05:00",
			"duration" : 1,
			"end" : "11pm",
			"location" : "Orchid Country Club",
			"name" : "Fozan Ali",
			"pitch" : 2,
			"rate" : 95,
			"start" : "10pm",
			"status" : "Paid",
			"sumittedDate" : "2020-02-27T13:17:09+08:00",
		}

failure_case_start_date_less = {
			"slotKey" : "-wowweareteating",
			"bookingKey" : "-wowweareteating",
			"date" : "2020-07-06T00:00:00+05:00",
			"duration" : 1,
			"end" : "11pm",
			"location" : "Orchid Country Club",
			"name" : "Fozan Ali",
			"pitch" : 2,
			"rate" : 95,
			"start" : "10pm",
			"status" : "Paid",
			"sumittedDate" : "2020-02-27T13:17:09+08:00",
		}

failure_case_end_date_less = {
			"slotKey" : "-wowweareteating",
			"bookingKey" : "-wowweareteating",
			"date" : "2020-10-12T00:00:00+05:00",
			"duration" : 1,
			"end" : "9pm",
			"location" : "Orchid Country Club",
			"name" : "Fozan Ali",
			"pitch" : 2,
			"rate" : 95,
			"start" : "10pm",
			"status" : "Paid",
			"sumittedDate" : "2020-02-27T13:17:09+08:00",
		}

failure_case_location_not_present = {
			"slotKey" : "-wowweareteating",
			"bookingKey" : "-wowweareteating",
			"date" : "2020-10-12T00:00:00+05:00",
			"duration" : 1,
			"end" : "9pm",
			"location" : "Orchid",
			"name" : "Fozan Ali",
			"pitch" : 2,
			"rate" : 95,
			"start" : "10pm",
			"status" : "Paid",
			"sumittedDate" : "2020-02-27T13:17:09+08:00",
		}

failure_case_data_not_valid = {
			"slotKey" : "-wowweareteating",
			"bookingKey" : "-wowweareteating",
			"date" : "2020-10-12T00:00:00+05:00",
			"duration" : 1,
			"end" : "9pm",
			"location" : "Orchid",
			"name" : "Fozan Ali",
			"pitch" : 2,
			"rate" : 95,
			"start" : "10pm",
			"status" : "Paid",
			"sumittedDate" : "hey this is a date",
		}

class BookingViewSetListTestCase(APITestCase):
	def setUp(self):
		api_key, key = APIKey.objects.create_key(name="bO4_UffT6FcimKuhY_qL-j")
		self.key = key

	def test_booking_list(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.get(reverse("booking-list"))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookingViewSetCreateTestCase(APITestCase):

	def setUp(self):
		api_key, key = APIKey.objects.create_key(name="bO4_UffT6FcimKuhY_qL-j")
		self.key = key

		location = Location(
			name="Orchid Country Club",
			lock_id="IGP1053e20f2"
		)
		location.save()

	def test_booking_create_success(self): 
		
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.post(reverse('booking-list'), success_case_data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_booking_missing_data(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.post(reverse('booking-list'), failure_case_missing_data)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_booking_start_date_less(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.post(reverse('booking-list'), failure_case_start_date_less)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_booking_end_date_less(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.post(reverse('booking-list'), failure_case_end_date_less)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_booking_location_not_present(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.post(reverse('booking-list'), failure_case_location_not_present)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_booking_data_not_valid(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.post(reverse('booking-list'), failure_case_data_not_valid)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookingViewSetUpdateTestCase(APITestCase):

	def setUp(self):
		api_key, key = APIKey.objects.create_key(name="bO4_UffT6FcimKuhY_qL-j")
		self.key = key

		location = Location(
			name="Orchid Country Club",
			lock_id="IGP1053e20f2"
		)
		location.save()

		self.booking = Booking(
			slotKey= "-wowweareteating",
			bookingKey= "-wowweareteating",
			date = "2020-07-20T00:00:00+05:00",
			duration = 1,
			end = "11pm",
			location = "Orchid Country Club",
			name = "Fozan Ali",
			pitch = 2,
			rate = 95,
			start = "10pm",
			status = "Paid",
			sumittedDate = "2020-02-27T13:17:09+08:00",
			email= "ali.gardezi@tintash.com"
		)
		self.booking.save()
	
	def test_booking_create_success(self): 
		
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.put(reverse('booking-detail', kwargs={"pk": 1}), success_case_data)

		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def test_booking_for_wrong_key_on_update(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.put(reverse('booking-detail', kwargs={"pk": 2}), success_case_data)

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_booking_missing_data_on_update(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.put(reverse('booking-detail', kwargs={"pk": 1}), failure_case_missing_data)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


	def test_booking_end_date_less_on_update(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.put(reverse('booking-detail', kwargs={"pk": 1}), failure_case_end_date_less)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_booking_location_not_present_on_update(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.put(reverse('booking-detail', kwargs={"pk": 1}), failure_case_location_not_present)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_booking_data_not_valid_on_update(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.put(reverse('booking-detail', kwargs={"pk": 1}), failure_case_data_not_valid)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BookingViewSetDeleteTestCase(APITestCase):

	def setUp(self):
		api_key, key = APIKey.objects.create_key(name="bO4_UffT6FcimKuhY_qL-j")
		self.key = key

		location = Location(
			name="Orchid Country Club",
			lock_id="IGP1053e20f2"
		)
		location.save()

		self.booking = Booking(
			slotKey= "-wowweareteating",
			bookingKey= "-wowweareteating",
			date = "2020-07-20T00:00:00+05:00",
			duration = 1,
			end = "11pm",
			location = "Orchid Country Club",
			name = "Fozan Ali",
			pitch = 2,
			rate = 95,
			start = "10pm",
			status = "Paid",
			sumittedDate = "2020-02-27T13:17:09+08:00",
			email= "ali.gardezi@tintash.com"
		)
		self.booking.save()
	
	def test_booking_for_wrong_key_on_delete(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.delete(reverse('booking-detail', kwargs={"pk": 2}), {
			"slotKey": "-wowweareteating",
			"sumittedDate": "2020-02-27T13:17:09+08:00"
		})

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_booking_for_wrong_slot_key_on_delete(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.delete(reverse('booking-detail', kwargs={"pk": 2}), {
			"slotKey": "-wowweareating",
			"sumittedDate": "2020-02-27T13:17:09+08:00"
		})

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_booking_success_on_delete(self):
		client.credentials(HTTP_AUTHORIZATION='Api-Key '+self.key)

		response = client.delete(reverse('booking-detail', kwargs={"pk": 1}), {
			"slotKey": "-wowweareteating",
			"sumittedDate": "2020-02-27T13:17:09+08:00"
		})

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# @TODO: Figure out a better location for this test class
class SchedulerTest(TestCase):
	
	def setUp(self):
		api_key, key = APIKey.objects.create_key(name="bO4_UffT6FcimKuhY_qL-j")
		self.key = key

		location = Location(
			name="Orchid Country Club",
			lock_id="IGP1053e20f2"
		)
		location.save()

		self.booking = Booking(
			slotKey= "-wowweareteating",
			bookingKey= "-wowweareteating",
			date = "2020-07-20T00:00:00+05:00",
			duration = 1,
			end = "11pm",
			location = "Orchid Country Club",
			name = "Fozan Ali",
			pitch = 2,
			rate = 95,
			start = "10pm",
			status = "Paid",
			sumittedDate = "2020-02-27T13:17:09+08:00",
			email= "ali.gardezi@tintash.com"
		)
		self.booking.save()

	def test_turn_light_on_success(self):
		data = TurnlightOnTask("bO4_UffT6FcimKuhY_qL-j", "-wowweareteating")
		self.assertEqual(data, True)

	def test_turn_light_on_failure(self):
		data = TurnlightOnTask("bO4_UffT6F", "-wowwearetea")
		self.assertEqual(data, False)

	def test_send_lock_code_success(self):
		data = sendLockCode("IGP1053e20f2", "2020-12-07 09:00:00", "2020-12-07 10:00:00", "test_email_ali_123123@gmail.com", "-wowweareteating")
		self.assertEqual(data, True)

	def test_send_lock_code_failure(self):
		data = sendLockCode("IGP1053e20f2", "2020-07-07 09:00:00", "2020-07-07 10:00:00", "est_email_ali_123123@gmail.com", "-wowweareteating")
		self.assertEqual(data, False)