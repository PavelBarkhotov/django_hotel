from django.http import HttpResponse, JsonResponse, Http404
from typing import Any
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BookingWriteSerializer, BookingReadSerializer, RoomWriteSerializer, RoomReadSerializer
from .models import Booking, Room


def index(request):
    return HttpResponse('<h1>Index page</h1>')


class CreateReturnIdAPIMixin(CreateAPIView):
    def create(self: GenericAPIView, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            {'id': serializer.instance.id},
            status=status.HTTP_201_CREATED
        )


class BookingCreateReturnIdAPIView(CreateReturnIdAPIMixin, CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingWriteSerializer


class BookingListAPIView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingReadSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['room']

class BookingRetrieveAPIView(RetrieveAPIView):
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

class RoomRetrieveAPIView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer


class RoomDestroyAPIView(DestroyAPIView):
    queryset = Room.objects.all()
