from django.contrib import admin
from .models import Booking, BookingSchedulerHistory

admin.site.register(Booking)
admin.site.register(BookingSchedulerHistory)

