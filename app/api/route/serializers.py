from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from ..helpers.serialization_errors import error_dict
from .models import Route


class SchedulingRouteSerializer(serializers.ModelSerializer):
    """Scheduling route serializer"""

    created_by =  serializers.SerializerMethodField()

    starting_point = PointField()

    destination = PointField()

    commuting_time = serializers.TimeField()

    @staticmethod
    def get_created_by(obj):
        return obj.id

    @staticmethod
    def validate_created_by(created_by_id):
        route = Route.objects.filter(created_by=created_by_id)
        if route:
            raise serializers.ValidationError(
                error_dict['existing_route']
            )

    class Meta:
        model = Route
        fields = ('created_by','destination','starting_point','commuting_time')
