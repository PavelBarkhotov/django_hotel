from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Room


@pytest.mark.django_db
class TestRoomCreateAPI:
    url = reverse("room-list")

    def test_create_room_success(self, api_client: APIClient) -> None:
        payload = {"description": "Deluxe Room", "price": 5000.00}

        response = api_client.post(self.url, data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert Room.objects.count() == 1

    def test_create_room_invalid_price(self, api_client: APIClient) -> None:
        payload = {"description": "Cheap Room", "price": -100.00}

        response = api_client.post(self.url, data=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "price" in response.data


@pytest.mark.django_db
class TestRoomListAPI:
    url = reverse("room-list")

    def test_get_room_list(self, api_client: APIClient, sample_room: Room) -> None:
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == sample_room.id


@pytest.mark.django_db
class TestRoomDetailAPI:
    def test_get_room_detail(self, api_client: APIClient, sample_room: Room) -> None:
        url = reverse("room-detail", args=[sample_room.id])

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == sample_room.id

    def test_get_room_not_found(self, api_client: APIClient) -> None:
        url = reverse("room-detail", args=[9999])

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_room_success(self, api_client: APIClient, sample_room: Room) -> None:
        url = reverse("room-detail", args=[sample_room.id])
        payload = {"price": 2500.00}

        response = api_client.patch(url, data=payload)

        assert response.status_code == status.HTTP_200_OK
        sample_room.refresh_from_db()
        assert float(sample_room.price) == 2500.00

    def test_delete_room(self, api_client: APIClient, sample_room: Room) -> None:
        url = reverse("room-detail", args=[sample_room.id])

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Room.objects.count() == 0
