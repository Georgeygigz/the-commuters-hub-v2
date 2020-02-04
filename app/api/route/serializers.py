from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from ..helpers.serialization_errors import error_dict
from .models import Route, Members
from ..vehicle.models import Vehicle
from ..vehicle.serializers import VehicleRetrieveSerializer
from ..authentication.serializers import UserSearchSerializer


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

class MembersRetrieveSerializer(serializers.ModelSerializer):

    member = UserSearchSerializer()

    def to_representation(self,instance):
        """
        Override the default to_representation
        to return values only

        Args:
            instace (obj) : current object reference
        """

        # get the instance -> Dict of primitive data types
        representation = super(MembersRetrieveSerializer,
                               self).to_representation(instance)

        # manipulate returned dictionary as desired
        member = representation.pop('member')
        return member

    class Meta:
        model = Members
        fields = ('member',)

class RouteRetrieveSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField()
    created_by =  UserSearchSerializer()
    vehicle = VehicleRetrieveSerializer()

    @staticmethod
    def get_members(obj):
        members_obj = Members.objects.filter(route=obj.id)
        members_serializer = MembersRetrieveSerializer(members_obj, many=True)
        return members_serializer.data

    class Meta:
        model = Route
        fields =     ('id', 'created_at', 'updated_at', 'deleted', 'starting_point',
                    'destination', 'vehicle', 'commuting_time', 'created_by','members')


class RouteUpdateSerializer(serializers.ModelSerializer):
    """Scheduling route serializer"""
    id = serializers.CharField(read_only=True)
    starting_point = PointField()

    destination = PointField()

    commuting_time = serializers.TimeField()

    vehicle =  serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Vehicle.objects.filter(),
        error_messages={'does_not_exist':
                        error_dict['does_not_exist'].format('Vehicle')})

    class Meta:
        model = Route
        fields =     ('id', 'starting_point', 'destination',
                    'commuting_time','vehicle')
