import datetime
from typing import Any

from rest_framework import serializers

from .models import Booking, Room


class BookingWriteSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(source="room", queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = ["room_id", "date_start", "date_end"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        room: Room | None = attrs.get("room", getattr(self.instance, "room", None))
        date_start: datetime.date | None = attrs.get(
            "date_start", getattr(self.instance, "date_start", None)
        )
        date_end: datetime.date | None = attrs.get(
            "date_end", getattr(self.instance, "date_end", None)
        )

        self._validate_dates(date_start, date_end)
        self._validate_overlapping(room, date_start, date_end)

        return attrs

    @staticmethod
    def _validate_dates(date_start: datetime.date | None, date_end: datetime.date | None) -> None:
        if date_start and date_end and date_start >= date_end:
            raise serializers.ValidationError(
                {"date_end": "Дата окончания брони должна быть больше даты начала"}
            )

    def _validate_overlapping(
        self, room: Room | None, date_start: datetime.date | None, date_end: datetime.date | None
    ) -> None:
        overlapping = Booking.objects.filter(
            room=room, date_start__lt=date_end, date_end__gt=date_start
        )

        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        if overlapping.exists():
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Указанный временной интервал пересекается с уже существующей записью."
                }
            )


class BookingReadSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(source="room", queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = ["id", "room_id", "date_start", "date_end"]


class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["description", "price"]


class RoomReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at", "updated_at"]
