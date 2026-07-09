from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Booking, Room


@pytest.mark.django_db
class TestBookingCreateAPI:
    url = reverse("booking-list")

    def test_create_booking_success(self, api_client: APIClient, sample_room: Room) -> None:
        payload = {"room_id": sample_room.id, "date_start": "2026-08-01", "date_end": "2026-08-05"}

        response = api_client.post(self.url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert Booking.objects.count() == 1

    def test_create_booking_overlap(
        self, api_client: APIClient, sample_room: Room, sample_booking: Booking
    ) -> None:
        payload = {"room_id": sample_room.id, "date_start": "2026-08-12", "date_end": "2026-08-18"}

        response = api_client.post(self.url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data
        assert Booking.objects.count() == 1

    def test_create_booking_invalid_dates(
        self, api_client: APIClient, sample_room: Room, sample_booking: Booking
    ) -> None:
        payload = {"room_id": sample_room.id, "date_start": "2026-08-20", "date_end": "2026-08-10"}

        response = api_client.post(self.url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "date_end" in response.data

    def test_create_booking_invalid_room(
        self, api_client: APIClient, sample_room: Room, sample_booking: Booking
    ) -> None:
        payload = {"room_id": 9999, "date_start": "2026-08-01", "date_end": "2026-08-05"}

        response = api_client.post(self.url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "room_id" in response.data


@pytest.mark.django_db
class TestBookingListAPI:
    url = reverse("booking-list")

    def test_get_bookings_list(self, api_client: APIClient, sample_booking: Booking) -> None:
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == sample_booking.id

    def test_get_booking_by_room(
        self, api_client: APIClient, sample_room: Room, sample_booking: Booking
    ) -> None:
        response = api_client.get(self.url, filter={"room": sample_room.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestBookingDetailAPI:
    def test_get_booking_detail(self, api_client: APIClient, sample_booking: Booking) -> None:
        url = reverse("booking-detail", args=[sample_booking.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == sample_booking.id

    def test_get_booking_detail_invalid_id(
        self, api_client: APIClient, sample_booking: Booking
    ) -> None:
        url = reverse("booking-detail", args=[9999])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_booking_detail(self, api_client: APIClient, sample_booking: Booking) -> None:
        url = reverse("booking-detail", args=[sample_booking.id])
        payload = {"date_start": "2026-08-09"}

        response = api_client.patch(url, data=payload)

        assert response.status_code == status.HTTP_200_OK
        sample_booking.refresh_from_db()
        assert str(sample_booking.date_start) == "2026-08-09"

    def test_update_booking_overlap(
        self, api_client: APIClient, sample_room: Room, sample_booking: Booking
    ) -> None:
        Booking.objects.create(room=sample_room, date_start="2026-08-20", date_end="2026-08-25")

        url = reverse("booking-detail", args=[sample_booking.id])
        payload = {"date_end": "2026-08-22"}

        response = api_client.patch(url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data

    def test_delete_booking(self, api_client: APIClient, sample_booking: Booking) -> None:
        url = reverse("booking-detail", args=[sample_booking.id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Booking.objects.count() == 0
