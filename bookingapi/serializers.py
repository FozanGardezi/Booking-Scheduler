from rest_framework import serializers

from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
		class Meta:
			model = Booking
			fields = (
				"id",
				"slotKey", 
				"bookingKey",
				"date",
				"duration",
				"end",
				"location",
				"name",
				"pitch",
				"rate",
				"start",
				"status",
				"sumittedDate",
				"email"
				)
