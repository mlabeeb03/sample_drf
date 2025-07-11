from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Booking, Vehicle


class VehicleViewTest(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create regular user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Create admin user
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            is_staff=True,
            is_superuser=True,
        )

        # Create test vehicle
        self.vehicle = Vehicle.objects.create(
            make="Toyota",
            model="Camry",
            year=2022,
            plate="ABC-123",
        )

        # URLs
        self.vehicle_list_url = reverse("vehicle-list")  # Adjust based on your URL name
        self.vehicle_detail_url = reverse(
            "vehicle-detail", kwargs={"pk": self.vehicle.pk}
        )

        # Client setup
        self.client = APIClient()

    def test_get_vehicle_list_as_admin(self):
        """Test retrieving vehicle list as admin"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.get("/vehicles/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["make"], "Toyota")

    def test_get_vehicle_list_as_regular_user(self):
        """Test retrieving vehicle list as regular user (should fail)"""
        # Authenticate as regular user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.get("/vehicles/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_vehicle_list_unauthenticated(self):
        """Test retrieving vehicle list without authentication"""
        response = self.client.get("/vehicles/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_vehicle_detail_as_admin(self):
        """Test retrieving specific vehicle as admin"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.get(f"/vehicles/{self.vehicle.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["make"], "Toyota")
        self.assertEqual(response.data["model"], "Camry")

    def test_get_vehicle_detail_not_found(self):
        """Test retrieving non-existent vehicle"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.get("/vehicles/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vehicle_as_admin(self):
        """Test creating vehicle as admin"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        data = {
            "make": "Honda",
            "model": "Civic",
            "year": 2021,
            "plate": "XYZ-789",
        }

        response = self.client.post("/vehicles/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["make"], "Honda")
        self.assertEqual(Vehicle.objects.count(), 2)

    def test_create_vehicle_as_regular_user(self):
        """Test creating vehicle as regular user (should fail)"""
        # Authenticate as regular user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        data = {
            "make": "Honda",
            "model": "Civic",
            "year": 2021,
            "plate": "XYZ-789",
        }

        response = self.client.post("/vehicles/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_vehicle_invalid_data(self):
        """Test creating vehicle with invalid data"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        data = {
            "make": "",  # Invalid - empty make
            "model": "Civic",
            "year": 2021,
            "plate": "XYZ-789",
        }

        response = self.client.post("/vehicles/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_vehicle_as_admin(self):
        """Test updating vehicle as admin"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        data = {
            "make": "Toyota",
            "model": "Corolla",  # Changed model
            "year": 2022,
            "plate": "ABC-123",
        }

        response = self.client.put(f"/vehicles/{self.vehicle.pk}/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["model"], "Corolla")

    def test_update_vehicle_not_found(self):
        """Test updating non-existent vehicle"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        data = {
            "make": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "plate": "ABC-123",
        }

        response = self.client.put("/vehicles/999/", data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vehicle_as_admin(self):
        """Test deleting vehicle as admin"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.delete(f"/vehicles/{self.vehicle.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 0)

    def test_delete_vehicle_not_found(self):
        """Test deleting non-existent vehicle"""
        # Authenticate as admin
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.delete("/vehicles/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookingListCreateViewTest(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="pass123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="pass123"
        )

        # Create vehicle
        self.vehicle = Vehicle.objects.create(
            make="Toyota",
            model="Camry",
            year=2022,
            plate="ABC-123",
        )

        # Create booking for user1
        self.booking = Booking.objects.create(
            vehicle=self.vehicle,
            user=self.user1,
            start_datetime="2023-12-01",
            end_datetime="2023-12-05",
        )

        self.client = APIClient()

    def test_get_bookings_authenticated_user(self):
        """Test retrieving bookings for authenticated user"""
        # Authenticate as user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.get("/bookings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["vehicle"], self.vehicle.pk)

    def test_get_bookings_different_user(self):
        """Test that user only sees their own bookings"""
        # Authenticate as user2
        refresh = RefreshToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.get("/bookings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # user2 has no bookings

    def test_get_bookings_unauthenticated(self):
        """Test retrieving bookings without authentication"""
        response = self.client.get("/bookings/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_authenticated_user(self):
        """Test creating booking as authenticated user"""
        # Authenticate as user2
        refresh = RefreshToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        data = {
            "vehicle": self.vehicle.pk,
            "start_datetime": "2023-12-10",
            "end_datetime": "2023-12-15",
        }

        response = self.client.post("/bookings/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user2.pk)
        self.assertEqual(Booking.objects.count(), 2)

    def test_create_booking_unauthenticated(self):
        """Test creating booking without authentication"""
        data = {
            "vehicle": self.vehicle.pk,
            "start_datetime": "2023-12-10",
            "end_datetime": "2023-12-15",
        }

        response = self.client.post("/bookings/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RegisterViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_valid_data(self):
        """Test user registration with valid data"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpass123",
            "password2": "strongpass123",  # Assuming your serializer requires password confirmation
        }

        response = self.client.post("/register/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "newuser")

    def test_register_invalid_data(self):
        """Test user registration with invalid data"""
        data = {
            "username": "",  # Empty username
            "email": "invalid-email",  # Invalid email
            "password": "123",  # Weak password
        }

        response = self.client.post("/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_duplicate_username(self):
        """Test registration with existing username"""
        # Create existing user
        User.objects.create_user(
            username="existinguser", email="existing@example.com", password="pass123"
        )

        data = {
            "username": "existinguser",  # Duplicate username
            "email": "new@example.com",
            "password": "strongpass123",
            "password2": "strongpass123",
        }

        response = self.client.post("/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)  # Still only one user


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client = APIClient()

    def test_login_valid_credentials(self):
        """Test login with valid credentials"""
        data = {"username": "testuser", "password": "testpass123"}

        response = self.client.post("/login/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {"username": "testuser", "password": "wrongpassword"}

        response = self.client.post("/login/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        data = {"username": "nonexistent", "password": "somepassword"}

        response = self.client.post("/login/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials")

    def test_login_missing_username(self):
        """Test login without username"""
        data = {"password": "testpass123"}

        response = self.client.post("/login/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_password(self):
        """Test login without password"""
        data = {"username": "testuser"}

        response = self.client.post("/login/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_empty_data(self):
        """Test login with empty data"""
        data = {}

        response = self.client.post("/login/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenRefreshViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()

    def test_token_refresh_valid(self):
        """Test token refresh with valid refresh token"""
        data = {"refresh": str(self.refresh)}

        response = self.client.post("/refresh/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_refresh_invalid(self):
        """Test token refresh with invalid refresh token"""
        data = {"refresh": "invalid_token"}

        response = self.client.post("/refresh/", data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_missing(self):
        """Test token refresh without refresh token"""
        data = {}

        response = self.client.post("/refresh/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
