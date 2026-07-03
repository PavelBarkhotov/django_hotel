from django.db import models


class Room(models.Model):
    class Meta:
        db_table = "rooms"

    description = models.CharField(max_length=255, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ночь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


class Booking(models.Model):
    class Meta:
        db_table = "bookings"

    room_id = models.ForeignKey(to=Room, verbose_name="ИД команты", on_delete=models.PROTECT)
    start_at = models.DateField(verbose_name="Дата начала брони")
    end_at = models.DateField(verbose_name="Дата окончания брони")
