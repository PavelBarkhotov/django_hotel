import datetime

from django.core.exceptions import ValidationError
import pytest

from ..models import Booking, Room
from ..services import create_booking, update_booking


@pytest.mark.django_db
class TestBookingServices:
    def test_create_booking_success(self, sample_room: Room) -> None:
        booking = create_booking(
            room=sample_room,
            date_start=datetime.date(2026, 8, 1),
            date_end=datetime.date(2026, 8, 5),
        )

        assert booking.id is not None
        assert booking.room == sample_room
        assert Booking.objects.count() == 1

    def test_create_booking_overlap(self, sample_room: Room, sample_booking: Booking) -> None:
        with pytest.raises(ValidationError):
            create_booking(
                room=sample_room,
                date_start=datetime.date(2026, 8, 12),
                date_end=datetime.date(2026, 8, 18),
            )

    def test_update_booking_success(self, sample_booking: Booking) -> None:
        updated_booking = update_booking(
            booking=sample_booking, date_start=datetime.date(2026, 8, 9)
        )

        assert updated_booking.date_start == datetime.date(2026, 8, 9)
        sample_booking.refresh_from_db()
        assert sample_booking.date_start == datetime.date(2026, 8, 9)

    def test_update_booking_self_overlap_ignored(self, sample_booking: Booking) -> None:
        updated_booking = update_booking(
            booking=sample_booking,
            date_start=datetime.date(2026, 8, 11),
            date_end=datetime.date(2026, 8, 16),
        )

        assert updated_booking.date_start == datetime.date(2026, 8, 11)
        assert updated_booking.date_end == datetime.date(2026, 8, 16)

    def test_update_booking_overlap_with_other(
        self, sample_room: Room, sample_booking: Booking
    ) -> None:
        Booking.objects.create(
            room=sample_room,
            date_start=datetime.date(2026, 8, 20),
            date_end=datetime.date(2026, 8, 25),
        )

        with pytest.raises(ValidationError):
            update_booking(booking=sample_booking, date_end=datetime.date(2026, 8, 22))
