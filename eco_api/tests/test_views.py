#PENISPEDICKA
import pytest
from rest_framework import status
from django.urls import reverse
from eco_api.models import Trip
from eco_api.serializers import TripSerializer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
  """Fixture to create an API client for testing."""
  return APIClient()

@pytest.fixture
def create_user():
  """Creates a user and returns it."""
  def _create_user(role='user', username="testuser", email="test@example.com"):
      user = User(username=username, email=email, role=role)
      user.set_password("testpass")
      user.save()
      return user
  return _create_user


def get_access_token(api_client, user):
  """Возвращает токен доступа для данного пользователя."""

  def _get_user_token(user):
      url = reverse("token_obtain_pair")
      data = {"username": user.username, "password": user.password}
      response = api_client.post(url, data, format="json")
      assert response.status_code == 200, f"Ошибка при получении токена: {response.content}"
      return response.json()["access"]

  return _get_user_token(user)



@pytest.mark.django_db
def test_get_trips_unauthorized(api_client):
   url = reverse("trip-list")
   response = api_client.get(url)
   assert response.status_code == status.HTTP_403_FORBIDDEN or response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_trips_authorized(api_client, create_user, get_access_token):
  user = create_user()
  token = get_access_token(api_client, user)
  url = reverse("trip-list")
  api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
  response = api_client.get(url)
  assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_trip_admin(api_client, create_user, get_access_token):
  user = create_user(role='admin')
  token = get_access_token(api_client, user)
  trip_data = {
      "start_date": "2024-01-15T10:00:00",
      "end_date": "2024-01-15T12:00:00",
      "transport_type": "car",
      "distance": 100.0,
      "passengers": 2,
      "energy_source": "gasoline"
  }
  url = reverse("trip-list")
  api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
  response = api_client.post(url, trip_data, format="json")
  assert response.status_code == status.HTTP_201_CREATED
  assert Trip.objects.count() == 1


@pytest.mark.django_db
def test_create_trip_editor(api_client, create_user, get_access_token):
  user = create_user(role='editor')
  token = get_access_token(api_client, user)
  trip_data = {
      "start_date": "2024-02-20T10:00:00",
      "end_date": "2024-02-20T12:00:00",
      "transport_type": "train",
      "distance": 200.0,
      "passengers": 1,
      "energy_source": "electricity"
  }
  url = reverse("trip-list")
  api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
  response = api_client.post(url, trip_data, format="json")
  assert response.status_code == status.HTTP_403_FORBIDDEN