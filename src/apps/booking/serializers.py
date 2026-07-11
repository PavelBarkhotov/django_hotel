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
        date_start: datetime.date | None = attrs.get(
            "date_start", getattr(self.instance, "date_start", None)
        )
        date_end: datetime.date | None = attrs.get(
            "date_end", getattr(self.instance, "date_end", None)
        )

        if date_start and date_end and date_start >= date_end:
            raise serializers.ValidationError(
                {"date_end": "Дата окончания брони должна быть строго позже даты начала"}
            )

        return attrs


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
