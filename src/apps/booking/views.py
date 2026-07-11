from django.core.exceptions import ValidationError as DjangoValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Booking, Room
from .serializers import (
    BookingReadSerializer,
    BookingWriteSerializer,
    RoomReadSerializer,
    RoomWriteSerializer,
)
from .services import create_booking, update_booking


class RoomViewSet(viewsets.ModelViewSet):
    """
    CRUD для управления комнатами.
    """

    queryset = Room.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "created_at"]
    ordering = ["created_at"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RoomWriteSerializer
        return RoomReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if serializer.instance is None:
            raise RuntimeError("Объект не был создан")

        return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.instance is None:
            raise RuntimeError("Объект не был обновлен")

        return Response({"id": serializer.instance.id}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Получить список бронирований по комнате",
        responses=BookingReadSerializer(many=True),
    )
    @action(detail=True, methods=["get"])
    def bookings(self, request, pk=None):
        room = self.get_object()
        bookings = room.booking_set.all()

        serializer = BookingReadSerializer(bookings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    CRUD для управления бронированиями.
    """

    queryset = Booking.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["room"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BookingWriteSerializer
        return BookingReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = create_booking(**serializer.validated_data)
            return Response({"id": booking.id}, status=status.HTTP_201_CREATED)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict if hasattr(e, "error_dict") else str(e)) from e

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            booking = update_booking(booking=instance, **serializer.validated_data)
            return Response({"id": booking.id}, status=status.HTTP_200_OK)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict if hasattr(e, "error_dict") else str(e)) from e
