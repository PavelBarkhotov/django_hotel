import datetime
from typing import Any

from django.core.exceptions import ValidationError

from .models import Booking, Room


def _check_dates_overlap(
    room: Room,
    date_start: datetime.date,
    date_end: datetime.date,
    exclude_booking_id: int | None = None,
) -> None:
    overlapping = Booking.objects.filter(
        room=room, date_start__lt=date_end, date_end__gt=date_start
    )

    if exclude_booking_id:
        overlapping = overlapping.exclude(pk=exclude_booking_id)

    if overlapping.exists():
        raise ValidationError(
            {
                "non_field_errors": "Указанный временной интервал пересекается с уже существующей записью."
            }
        )


def create_booking(*, room: Room, date_start: datetime.date, date_end: datetime.date) -> Booking:
    _check_dates_overlap(room, date_start, date_end)
    return Booking.objects.create(room=room, date_start=date_start, date_end=date_end)


def update_booking(*, booking: Booking, **data: Any) -> Booking:
    room = data.get("room", booking.room)
    date_start = data.get("date_start", booking.date_start)
    date_end = data.get("date_end", booking.date_end)

    _check_dates_overlap(room, date_start, date_end, exclude_booking_id=booking.pk)

    for field, value in data.items():
        setattr(booking, field, value)

    booking.save()
    return booking
