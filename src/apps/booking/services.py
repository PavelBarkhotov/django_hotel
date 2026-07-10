import datetime
import logging
from typing import Any

from django.core.exceptions import ValidationError

from .models import Booking, Room

logger = logging.getLogger(__name__)


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
        logger.warning(
            "Попытка создать пересекающееся бронирование.",
            extra={"date_start": date_start, "date_end": date_end, "room_id": room.id},
        )
        raise ValidationError(
            {
                "non_field_errors": "Указанный временной интервал пересекается с уже существующей записью."
            }
        )


def create_booking(*, room: Room, date_start: datetime.date, date_end: datetime.date) -> Booking:
    logger.info(
        "Начало создания бронирования для комнаты",
        extra={"room_id": room.id, "date_start": date_start, "date_end": date_end},
    )
    _check_dates_overlap(room, date_start, date_end)

    booking = Booking.objects.create(room=room, date_start=date_start, date_end=date_end)
    logger.info(
        "Бронирование успешно создано для комнаты",
        extra={"booking_id": booking.id, "room_id": room.id},
    )
    return booking


def update_booking(*, booking: Booking, **data: Any) -> Booking:
    logger.info("Попытка обновления бронирования", extra={"booking_id": booking.id})
    room = data.get("room", booking.room)
    date_start = data.get("date_start", booking.date_start)
    date_end = data.get("date_end", booking.date_end)

    _check_dates_overlap(room, date_start, date_end, exclude_booking_id=booking.pk)

    for field, value in data.items():
        setattr(booking, field, value)

    booking.save()
    logger.info("Обновление бронирования прошло успешно", extra={"booking_id": booking.id})
    return booking
