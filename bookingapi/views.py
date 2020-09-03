from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey

from django.utils import timezone
from django.forms.models import model_to_dict
from django.http import JsonResponse

from mysite.scheduler.scheduler_jobs import TurnlightOnTask, TurnlightOffTask, sendLockCode
from mysite.utils.http_util import get_Authorization_token
from mysite.utils.date_util import formatDateAccordingToHour, getDateAccordingToHour, addDays, formatDate, subtractMinutes
from core.scheduler import scheduler
from django.conf import settings

from .serializers import BookingSerializer
from .models import Booking
from location.models import Location

class BookingViewSet(viewsets.ModelViewSet):
	queryset = Booking.objects.all().order_by('name')
	serializer_class = BookingSerializer

	permission_classes = [HasAPIKey]

	@staticmethod
	def get_date(request):
		start_date = getDateAccordingToHour(request.data.get("date"), request.data.get("start"))
		end_date = getDateAccordingToHour(request.data.get("date"), request.data.get("end"))
		return start_date, end_date		


	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		slot_key = request.data.get("slotKey")
		key = get_Authorization_token(request)

		#if data already exist return it 
		if (Booking.objects.filter(slotKey=slot_key).exists()): 
			booking_data = Booking.objects.get(slotKey=slot_key);
			data_response = JsonResponse(model_to_dict(booking_data));
			return data_response

		ifttt_key = APIKey.objects.get_from_key(key)

		start_date, end_date = self.get_date(request)

		booking_data = super(BookingViewSet, self).create(request, *args, **kwargs) # move it up before scheduler 
		# Throw error if start date is less then current time 
		if (start_date < timezone.now()):
			return Response(data={"start": ["start cannot be less then current time value"]},status=status.HTTP_400_BAD_REQUEST)

		# Throw error if end date is less then start time 
		if (end_date < start_date):
			return Response(data={"end": ["end cannot be less then start"]},status=status.HTTP_400_BAD_REQUEST)

		location = Location.objects.filter(name = request.data.get("location"))

		# Throw error if this date does not exists in our database
		if location.count() == 0: 
			return Response(data={"detail": "This location is not supported. Please add this location first before making a booking"},status=status.HTTP_400_BAD_REQUEST)

		lock_time = subtractMinutes(start_date, settings.EMAIL_TIME)

		start_date = formatDate(start_date, '%Y-%m-%d %H:%M:%S')
		scheduler.add_job(TurnlightOnTask, "interval", { ifttt_key.name, slot_key }, start_date=start_date, end_date=start_date, id=slot_key+"_start")

		end_date = formatDate(end_date, '%Y-%m-%d %H:%M:%S')
		scheduler.add_job(TurnlightOffTask, "interval", { ifttt_key.name, slot_key }, start_date=end_date, end_date=end_date, id=slot_key+"_end")

		lock_id = location[0].lock_id
		email = request.data.get("email")
		if (lock_time < timezone.now()):
			sendLockCode(lock_id, start_date, end_date, email, slot_key)
		else: 	
			scheduler.add_job(sendLockCode, "interval", { lock_id, start_date, end_date, email, slot_key }, start_date=lock_time, end_date=lock_time, id=slot_key+"_lock")
		
		return booking_data

	def update(self, request, *args, **kwargs):
		if Booking.objects.filter(id = kwargs['pk'], slotKey = request.data.get("slotKey")).count() == 0: 
			return Response(data={"detail": "Not found."},status=status.HTTP_404_NOT_FOUND)
		
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		start_date, end_date = self.get_date(request)

		booking_data = super(BookingViewSet, self).update(request, *args, **kwargs)

		if (end_date < start_date):
			return Response(data={"end": ["end cannot be less then start"]},status=status.HTTP_400_BAD_REQUEST)

		location = Location.objects.filter(name = request.data.get("location"))
		if location.count() == 0: 
			return Response(data={"detail": "Updated location is not supported. Please add this location first before updating a booking"},status=status.HTTP_400_BAD_REQUEST)

		slot_key = request.data.get("slotKey")
		key = get_Authorization_token(request)
		
		ifttt_key = APIKey.objects.get_from_key(key)
		
		start_job = scheduler.get_job(slot_key+"_start")
		if start_job != None:
			# removing job becasue we cannot update the starte and end date due to which 
			# we need to remove the job and create a new one
			scheduler.remove_job(slot_key+"_start")
			if start_date >= timezone.now():
				start_date = formatDate(start_date, '%Y-%m-%d %H:%M:%S')
				scheduler.add_job(TurnlightOnTask, "interval", { ifttt_key.name, slot_key }, start_date=start_date, end_date=start_date, id=slot_key+"_start")
		
		end_date = formatDate(end_date, '%Y-%m-%d %H:%M:%S')
		end_job = scheduler.get_job(slot_key+"_end")
		if end_job != None:
			scheduler.remove_job(slot_key+"_end")
			scheduler.add_job(TurnlightOffTask, "interval", { ifttt_key.name, slot_key }, start_date=end_date, end_date=end_date, id=slot_key+"_end")

		lock_data = scheduler.get_job(slot_key+"_lock")
		lock_time = subtractMinutes(start_date, settings.EMAIL_TIME)
		email = request.data.get("email")
		if lock_data != None:
			if lock_time < timezone.now():
				scheduler.add_job(sendLockCode, "interval", { lock_id, start_date, end_date, email, slot_key }, start_date=lock_time, end_date=lock_time, id=slot_key+"_lock")
			else:
				sendLockCode(lock_id, start_date, end_date, email, slot_key)

		return booking_data

	def destroy(self, request, *args, **kwargs):
		if Booking.objects.filter(id = kwargs['pk'], slotKey = request.data.get("slotKey")).count() == 0: 
			return Response(data={"detail": "Not found."},status=status.HTTP_404_NOT_FOUND)

		slot_key = request.data.get("slotKey")
		if slot_key is None: 
			return Response(data={"slotKey": ["This field is required"]},status=status.HTTP_400_BAD_REQUEST)

		if  type(slot_key) != str:
			return Response(data={"slotKey": ["A valid string is required"]},status=status.HTTP_400_BAD_REQUEST)

		start_job = scheduler.get_job(slot_key+"_start")
		if start_job != None:
			scheduler.remove_job(slot_key+"_start")

		end_job = scheduler.get_job(slot_key+"_end")
		if end_job != None:
			scheduler.remove_job(slot_key+"_end")

		lock_job = scheduler.get_job(slot_key+"_lock")
		if lock_job != None: 
			scheduler.remove_job(slot_key+"_lock")

		instance = self.get_object()
		self.perform_destroy(instance)

		return Response(status=status.HTTP_204_NO_CONTENT)
