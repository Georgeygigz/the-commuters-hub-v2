from django.contrib.gis.geos import fromstr
from rest_framework.serializers import ValidationError
from ..models import Route
from ...helpers.serialization_errors import error_dict


def get_location_points(request_data):
    starting_point_longitude = request_data['starting_point'].get('longitude',0)
    starting_point_latitude = request_data['starting_point'].get('latitude',0)

    destination_point_longitude = request_data['destination'].get('longitude',0)
    destination_point_latitude = request_data['destination'].get('latitude',0)

    starting_point = fromstr(
        f'POINT({starting_point_longitude} {starting_point_latitude})', srid=4326)
    destination = fromstr(
        f'POINT({destination_point_longitude} {destination_point_latitude})', srid=4326)
    return starting_point, destination


def validate_route(request_data):
    starting_point, destination = get_location_points(request_data)
    route = Route.objects.filter(starting_point=starting_point,
                                destination=destination )
    if route:
        raise ValidationError(
        error_dict['route_exist']
    )
