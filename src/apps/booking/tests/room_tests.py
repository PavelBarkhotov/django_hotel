from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.booking.models import Room


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_rooms():
    return Room.objects.create(description="1_test_description", price=1111.11)


@pytest.mark.django_db
def test_create_room(api_client):
    url = reverse("api_room_create")
    data = {"description": "first_test", "price": 1234.56}

    response = api_client.post(url, data, format="json")
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data


@pytest.mark.django_db
def test_get_room_list(api_client, sample_rooms):
    url = reverse("api_room_list")

    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["description"] == sample_rooms.description
    assert response.data[0]["price"] == str(sample_rooms.price)


@pytest.mark.django_db
def test_get_room(api_client, sample_rooms):
    url = reverse("api_room_solo", args=str(sample_rooms.id))

    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == sample_rooms.description
    assert response.data["price"] == str(sample_rooms.price)


@pytest.mark.django_db
def test_update_room(api_client, sample_rooms):
    url = reverse("api_room_update", args=str(sample_rooms.id))
    data = {"description": "updated_description", "price": 6543.21}

    response = api_client.put(url, data, format="json")

    sample_rooms.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == sample_rooms.id
    assert response.data["description"] == sample_rooms.description
    assert response.data["price"] == str(sample_rooms.price)


@pytest.mark.django_db
def test_delete_room(api_client, sample_rooms):
    url = reverse("api_room_delete", kwargs={"pk": str(sample_rooms.id)})

    response = api_client.delete(url, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
