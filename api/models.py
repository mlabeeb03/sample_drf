from django.contrib.auth.models import User
from django.db import models


class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    vehicle = models.ForeignKey(
        "Vehicle", on_delete=models.CASCADE, related_name="bookings"
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"Booking for {self.vehicle} by {self.user} from {self.start_datetime} to {self.end_datetime}"
