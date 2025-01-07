import pytest
from rest_framework import status
from django.urls import reverse
from eco_api.models import Trip
from eco_api.serializers import TripSerializer
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Fixture to create an API client for testing."""
    return APIClient()


@pytest.fixture
def create_user():
    """Creates a user and returns it."""
    from django.contrib.auth import get_user_model

    def _create_user(role='user', username="testuser", email="test@example.com"):
        User = get_user_model()
        user = User(username=username, email=email)
        user.set_password("testpass")
        setattr(user, 'role', role)  # <-- Устанавливаем role через setattr()
        user.save()
        return user

    return _create_user


@pytest.fixture
def get_access_token(api_client, create_user):
    """Returns an access token for the given user."""

    def _get_access_token(user):
        url = reverse("token_obtain_pair")
        data = {"username": user.username, "password": "testpass"}
        response = api_client.post(url, data, format="json")
        print(response.json())  # <-- Вывод для отладки
        return response.json()["access"]

    return _get_access_token


@pytest.mark.django_db
def test_get_trips_unauthorized(api_client):
    url = reverse("trip-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_trips_authorized(api_client, create_user, get_access_token):
    user = create_user()  # <-- убрали передачу role
    token = get_access_token(user)
    url = reverse("trip-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_trip_admin(api_client, create_user, get_access_token):
    user = create_user(role='admin')  # <--- Добавили роль
    token = get_access_token(user)
    trip_data = {
        "start_date": "2024-01-15T10:00:00",
        "end_date": "2024-01-15T12:00:00",
        "transport_type": "car",
        "distance": 100.0,
        "passengers": 2,
        "energy_source": "gasoline"
    }
    print(trip_data)  # <-- Вывод trip_data для проверки
    url = reverse("trip-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.post(url, trip_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Trip.objects.count() == 1


@pytest.mark.django_db
def test_create_trip_editor(api_client, create_user, get_access_token):
    user = create_user(role='editor')  # <--- Добавили роль
    token = get_access_token(user)
    trip_data = {
        "start_date": "2024-02-20T10:00:00",
        "end_date": "2024-02-20T12:00:00",
        "transport_type": "train",
        "distance": 200.0,
        "passengers": 1,
        "energy_source": "electricity"
    }
    print(trip_data)  # <-- Вывод trip_data для проверки
    url = reverse("trip-list")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.post(url, trip_data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN