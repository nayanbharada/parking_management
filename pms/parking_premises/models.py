from django.db import models
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from users.models import UserMaster
# Create your models here.


class Premises(TimeStampedModel, ActivatorModel):
    premise_user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name='premise_users')
    premise_name = models.CharField(max_length=50)
    address = models.TextField()
    authorized_person_name = models.CharField(max_length=25)
    authorized_person_contact = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.premise_name}'


class Slot(TimeStampedModel, ActivatorModel):
    CAR = "car"
    TWO_WHEELER = "two_wheeler"
    THREE_WHEELER = "three_wheeler"

    VEHICLE_TYPE = (
        (CAR, "Car"),
        (TWO_WHEELER, "Two wheeler"),
        (THREE_WHEELER, "Three wheeler"),
    )
    premise_slot = models.ForeignKey(Premises, on_delete=models.CASCADE, related_name="premises_slots")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.vehicle_type} - {self.price}"


class BookParking(TimeStampedModel, ActivatorModel):
    slot_book = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="slot_books")
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name="user_bookings")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()