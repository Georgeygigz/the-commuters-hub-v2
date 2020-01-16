from django.db import models
from ..authentication.models import User
from app.api.models import BaseModel

class Vehicle(BaseModel):
    """
    Vehicle model
    """

    AVAILABLE = 'available'
    BOOKED = 'booked'

    VEHICLE_STATUS = [
        (AVAILABLE, 'ok'),
        (BOOKED, 'pending'),
    ]

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE, related_name="owner")

    registration_number = models.CharField(db_index=True, max_length=255, unique=True)

    capacity =  models.CharField(db_index=True, max_length=255, unique=False)

    status =  models.CharField(blank=False, max_length=20,
                             choices=VEHICLE_STATUS, default=AVAILABLE)

    trips =  models.CharField(db_index=True, max_length=255, unique=False)
