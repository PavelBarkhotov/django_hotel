import datetime

import pytest
from rest_framework.test import APIClient

from apps.booking.models import Booking, Room


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def sample_room(db: None) -> Room:
    return Room.objects.create(description="Standard Room", price=1500.00)


@pytest.fixture
def sample_booking(db: None, sample_room: Room) -> Booking:
    return Booking.objects.create(
        room=sample_room,
        date_start=datetime.date(2026, 8, 10),
        date_end=datetime.date(2026, 8, 15),
    )
