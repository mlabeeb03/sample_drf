from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import BookingListCreateView, LoginView, RegisterView, VehicleView

urlpatterns = [
    path("vehicles/", VehicleView.as_view()),
    path("vehicles/<int:pk>/", VehicleView.as_view()),
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
