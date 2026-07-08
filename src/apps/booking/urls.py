from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path(
        "bookings/create/", views.BookingCreateReturnIdAPIView.as_view(), name="api_booking_create"
    ),
    path("bookings/list/", views.BookingListAPIView.as_view(), name="api_booking_list"),
    path("bookings/<int:pk>/", views.BookingRetrieveAPIView.as_view(), name="api_booking_solo"),
    path(
        "bookings/<int:pk>/update/", views.BookingUpdateAPIView.as_view(), name="api_booking_update"
    ),
    path(
        "bookings/<int:pk>/delete/",
        views.BookingDestroyAPIView.as_view(),
        name="api_booking_delete",
    ),
    # api для комнат
    path("rooms/create/", views.RoomCreateReturnIdAPIView.as_view(), name="api_room_create"),
    path("rooms/list/", views.RoomListAPIView.as_view(), name="api_room_list"),
    path("rooms/<int:pk>/", views.RoomRetrieveAPIView.as_view(), name="api_room_solo"),
    path("rooms/<int:pk>/update/", views.RoomUpdateAPIView.as_view(), name="api_room_update"),
    path("rooms/<int:pk>/delete/", views.RoomDestroyAPIView.as_view(), name="api_room_delete"),
]
