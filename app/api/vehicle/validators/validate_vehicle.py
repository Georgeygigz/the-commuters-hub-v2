from rest_framework.serializers import ValidationError
from ..models import Vehicle
from ...helpers.serialization_errors import error_dict


def validate_vehicle_id(user_id, vehicle_id):
    """Validate that the vehicle exist
    Args:
        vehicle_id (str): the vehicle id
    Raises:
        Raise a validation error if vehicle id
        does not exist
    Return:
        vehicle (obj): the vehicle object
    """
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
        if vehicle.owner.id != user_id:
            raise ValidationError(
                error_dict['object_permission_denied'].format("vehicle"),
            )
        return vehicle

    except Vehicle.DoesNotExist:
        raise ValidationError(
            error_dict['does_not_exist'].format("Vehicle"),
        )
