from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.booking.models import Booking, Room


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_booking():
    room = Room.objects.create(description="1_test_description", price=1111.11)
    booking = Booking.objects.create(
        room_id=room.id, date_start="2025-01-01", date_end="2025-02-01"
    )
    return room, booking


@pytest.mark.django_db
def test_create_booking(api_client, sample_booking):
    room, booking = sample_booking
    url = reverse("api_booking_create")
    data = {"room_id": room.id, "date_start": "2025-03-01", "date_end": "2025-04-01"}

    response = api_client.post(url, data, format="json")
    print(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data


@pytest.mark.django_db
def test_get_booking_list(api_client, sample_booking):
    _, booking = sample_booking
    url = reverse("api_booking_list")

    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["room_id"] == booking.room.id
    assert response.data[0]["date_start"] == booking.date_start
    assert response.data[0]["date_end"] == booking.date_end


@pytest.mark.django_db
def test_get_booking(api_client, sample_booking):
    _, booking = sample_booking
    url = reverse("api_booking_solo", args=str(booking.id))

    response = api_client.get(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["room_id"] == booking.room.id
    assert response.data["date_start"] == booking.date_start
    assert response.data["date_end"] == booking.date_end


@pytest.mark.django_db
def test_update_booking(api_client, sample_booking):
    room, booking = sample_booking
    url = reverse("api_booking_update", args=str(booking.id))
    data = {"room_id": room.id, "date_start": "2025-01-01", "date_end": "2025-02-01"}

    response = api_client.put(url, data, format="json")

    booking.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == booking.id
    assert response.data["room_id"] == booking.room.id
    assert response.data["date_start"] == str(booking.date_start)
    assert response.data["date_end"] == str(booking.date_end)


@pytest.mark.django_db
def test_delete_booking(api_client, sample_booking):
    _, booking = sample_booking
    url = reverse("api_booking_delete", args=str(booking.id))

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
