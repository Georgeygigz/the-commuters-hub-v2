from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import Vehicle
from ..helpers.serialization_errors import error_dict
from ..authentication.serializers import UserSearchSerializer


class VehicleRegistrationSerializer(serializers.ModelSerializer):
    """Scheduling route serializer"""

    owner =  serializers.CharField(read_only=True)

    registration_number = serializers.CharField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=Vehicle.objects.all(),
                message=error_dict['already_exist'].format("Vehicle"),
            )
        ],
    )

    capacity =  serializers.CharField(required=True,
                                    allow_null=False)


    @staticmethod
    def get_owner(obj):
        """
        get the vehicle owner object
        Args:
            obj (object): current object reference
        Return:
            (obj): The owner object
        """
        return obj.id


    class Meta:
        model = Vehicle
        fields = ('owner','registration_number','capacity')



class VehicleUpdateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    registration_number = serializers.CharField()
    status = serializers.CharField(read_only=True)
    capacity = serializers.CharField()
    trips = serializers.CharField()
    fare = serializers.FloatField()

    class Meta:
        model = Vehicle
        fields = ('id','owner','registration_number','capacity','trips','fare','status')

class VehicleRetrieveSerializer(VehicleUpdateSerializer):
    owner = UserSearchSerializer()

    class Meta:
        model = Vehicle
        fields = ('id','owner','registration_number','capacity','trips','fare', 'status')
