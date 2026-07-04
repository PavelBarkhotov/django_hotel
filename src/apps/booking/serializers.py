from rest_framework import serializers

from .models import Booking, Room


class BookingWriteSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(source="room", queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = ["room_id", "date_start", "date_end"]


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
