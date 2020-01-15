from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from ..helpers.serialization_errors import error_dict
from .models import Route, Members


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


class MemberSerializer(serializers.ModelSerializer):

    route = serializers.PrimaryKeyRelatedField(
                    required=True,
                    queryset=Route.objects.filter(),
                    error_messages={'does_not_exist':
                        error_dict['does_not_exist'].format('recipient')})

    member =  serializers.CharField(read_only=True)

    @staticmethod
    def get_member(obj):
        """
        get the requester object
        Args:
            obj (object): current object reference
        Return:
            (obj): The requester object
        """
        return obj.id

    @staticmethod
    def validate_member(route_id,member_id):
        member = Members.objects.filter(
                    route=route_id,member=member_id)
        if member:
            raise serializers.ValidationError(
                error_dict['exit_in_route']
            )

    class Meta:
        model = Members
        fields = ('route','member')
