# Vehicle Booking API Documentation

## Overview
This API provides endpoints for managing vehicles and bookings in a vehicle rental system. It includes user authentication, vehicle management, and booking functionality.

## Installation Steps

### 1. Clone and Setup
```bash
git clone https://github.com/mlabeeb03/sample_drf
cd sample_drf
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Server
```bash
python manage.py runserver
```

The API can be accessed by making requests at: `http://localhost:8000/` using Postman, cURL etc.

## Running Tests
```bash
# Run all tests
python manage.py test
```

## Base URL
```
/
```

## Authentication
The API uses JWT (JSON Web Token) authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

## Endpoints

### Authentication

#### Register User
Creates a new user account.

- **URL**: `/register/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```
- **Response**:
  - **201 Created**: User successfully created
  - **400 Bad Request**: Invalid data

#### Login
Authenticates user and returns JWT tokens.

- **URL**: `/login/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **Response**:
  - **200 OK**:
    ```json
    {
      "refresh": "string",
      "access": "string"
    }
    ```
  - **401 Unauthorized**: Invalid credentials

#### Refresh Token
Refreshes the access token using the refresh token.

- **URL**: `/refresh/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "refresh": "string"
}
```
- **Response**:
  - **200 OK**:
    ```json
    {
      "access": "string"
    }
    ```
  - **401 Unauthorized**: Invalid refresh token

### Vehicles

#### List All Vehicles
Retrieves all vehicles in the system.

- **URL**: `/vehicles/`
- **Method**: `GET`
- **Authentication**: Required (Admin only)
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 1,
        "make": "string",
        "model": "string",
        "plate": "string",
      }
    ]
    ```
  - **401 Unauthorized**: Authentication required
  - **403 Forbidden**: Admin access required

#### Get Vehicle by ID
Retrieves a specific vehicle by its ID.

- **URL**: `/vehicles/{id}/`
- **Method**: `GET`
- **Authentication**: Required (Admin only)
- **Path Parameters**:
  - `id` (integer): Vehicle ID
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": 1,
      "make": "string",
      "model": "string",
      "year": 2023,
      "plate": "string",
    }
    ```
  - **401 Unauthorized**: Authentication required
  - **403 Forbidden**: Admin access required
  - **404 Not Found**: Vehicle not found

#### Create Vehicle
Creates a new vehicle in the system.

- **URL**: `/vehicles/`
- **Method**: `POST`
- **Authentication**: Required (Admin only)
- **Request Body**:
```json
{
  "make": "string",
  "model": "string",
  "year": 2023,
  "plate": "string",
}
```
- **Response**:
  - **201 Created**: Vehicle successfully created
  - **400 Bad Request**: Invalid data
  - **401 Unauthorized**: Authentication required
  - **403 Forbidden**: Admin access required

#### Update Vehicle
Updates an existing vehicle.

- **URL**: `/vehicles/{id}/`
- **Method**: `PUT`
- **Authentication**: Required (Admin only)
- **Path Parameters**:
  - `id` (integer): Vehicle ID
- **Request Body**:
```json
{
  "make": "string",
  "model": "string",
  "year": 2023,
  "plate": "string",
}
```
- **Response**:
  - **200 OK**: Vehicle successfully updated
  - **400 Bad Request**: Invalid data
  - **401 Unauthorized**: Authentication required
  - **403 Forbidden**: Admin access required
  - **404 Not Found**: Vehicle not found

#### Delete Vehicle
Deletes a vehicle from the system.

- **URL**: `/vehicles/{id}/`
- **Method**: `DELETE`
- **Authentication**: Required (Admin only)
- **Path Parameters**:
  - `id` (integer): Vehicle ID
- **Response**:
  - **204 No Content**: Vehicle successfully deleted
  - **401 Unauthorized**: Authentication required
  - **403 Forbidden**: Admin access required
  - **404 Not Found**: Vehicle not found

### Bookings

#### List User Bookings
Retrieves all bookings for the authenticated user.

- **URL**: `/bookings/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": 1,
        "vehicle": 1,
        "user": 1,
        "start_date": "2023-12-01",
        "end_date": "2023-12-05",
      }
    ]
    ```
  - **401 Unauthorized**: Authentication required

#### Create Booking
Creates a new booking for the authenticated user.

- **URL**: `/bookings/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
```json
{
  "vehicle": 1,
  "start_date": "2023-12-01",
  "end_date": "2023-12-05"
}
```
- **Response**:
  - **201 Created**: Booking successfully created
  - **400 Bad Request**: Invalid data or booking conflict
  - **401 Unauthorized**: Authentication required

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Data Models

### Vehicle
- `id`: Integer (auto-generated)
- `make`: String
- `model`: String
- `year`: Integer
- `plate`: String

### Booking
- `id`: Integer (auto-generated)
- `vehicle`: Integer (Foreign Key to Vehicle)
- `user`: Integer (Foreign Key to User)
- `start_date`: Date
- `end_date`: Date

### User
- `id`: Integer (auto-generated)
- `username`: String
- `email`: String
- `password`: String (hashed)
