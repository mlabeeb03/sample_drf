from django.contrib import admin

from .models import Booking, Vehicle

admin.site.register(Vehicle)
admin.site.register(Booking)
