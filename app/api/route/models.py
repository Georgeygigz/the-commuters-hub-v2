from django.contrib.gis.db import models
from ..helpers.push_id import PushID
from ..authentication.models import User
from app.api.models import BaseModel

class Route(models.Model):
    """
    The common field in all the models are defined here
    """
    # Add id to every entry in the database
    id = models.CharField(db_index=True, max_length=255,
                          unique=True, primary_key=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # add deleted option for every entry
    deleted = models.BooleanField(default=False)

    created_by =  models.ForeignKey(User,on_delete=models.CASCADE,
                        related_name="created_by",
                        unique=True)

    starting_point = models.PointField()

    destination = models.PointField()

    commuting_time = models.TimeField()


    def save(self,*args, **kwargs): # pylint: disable=W0221
        push_id = PushID()
        # This to check if it creates a new or updates an old instance
        if not self.id:
            self.id = push_id.next_id()
        super(Route, self).save() # pylint: disable=W0221


class Members(BaseModel):
    route = models.ForeignKey(Route,
                              on_delete=models.CASCADE, related_name="route")

    member = models.ForeignKey(User,
                               on_delete=models.CASCADE, related_name="member")
