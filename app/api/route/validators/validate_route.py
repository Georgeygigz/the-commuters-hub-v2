from rest_framework.serializers import ValidationError
from ..models import Route
from ...helpers.serialization_errors import error_dict


def validate_route_id(route_id):
    """Validate that the route exist
    Args:
        route_id (str): the route id
    Raises:
        Raise a validation error if route id
        does not exist
    Return:
        route (obj): the route object
    """
    try:
        route = Route.objects.get(id=route_id)
        return route

    except Route.DoesNotExist:
        raise ValidationError(
            error_dict['does_not_exist'].format("Route"),
        )
