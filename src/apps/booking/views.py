from typing import Any

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Booking, Room
from .serializers import (
    BookingReadSerializer,
    BookingWriteSerializer,
    RoomReadSerializer,
    RoomWriteSerializer,
)


def index(request):
    return HttpResponse("<h1>Index page</h1>")


class CreateReturnIdAPIMixin(CreateAPIView):
    def create(self: CreateAPIView, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        if serializer.instance:
            return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)
        else:
            raise NotFound("Объект не найден")


class BookingCreateReturnIdAPIView(CreateReturnIdAPIMixin, CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingWriteSerializer


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingReadSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["room"]


class BookingRetrieveAPIView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingReadSerializer


class BookingUpdateAPIView(CreateReturnIdAPIMixin, UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingReadSerializer


class BookingDestroyAPIView(DestroyAPIView):
    queryset = Booking.objects.all()


class RoomCreateReturnIdAPIView(CreateReturnIdAPIMixin, CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomWriteSerializer


class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer

    filter_backends = [OrderingFilter]
    ordering_fields = ["price", "created_at"]
    ordering = ["created_at"]


class RoomRetrieveAPIView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer


class RoomUpdateAPIView(CreateReturnIdAPIMixin, UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer


class RoomDestroyAPIView(DestroyAPIView):
    queryset = Room.objects.all()
