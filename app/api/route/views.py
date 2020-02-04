from rest_framework import status
from rest_framework import viewsets,generics, mixins
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from ..helpers.renderers import RequestJSONRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import (SchedulingRouteSerializer, MemberSerializer,
                        RouteRetrieveSerializer, RouteUpdateSerializer)
from ..helpers.constants import (REQUEST_SUCCESS_MESSAGE,
                                JOINED_ROUTE_SUCCESS_MESSAGE)
from .validators.route import validate_route
from ..helpers.route_members import add_route_member
from .models import Route
from ..helpers.pagination_helper import Pagination
from .validators.validate_route import validate_route_id

# Create your views here.
class ScheduleRouteApiView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = SchedulingRouteSerializer

    def post(self, request):
        """
        Overide the default post()
        """

        request_data = request.data
        serializer = self.serializer_class(data=request_data)

        serializer.validate_created_by(request.user.id)
        validate_route(request_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)

        # add user to the route members list
        add_route_member(request)

        return_message = {'message': REQUEST_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)


class RouteJoinAPiView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = MemberSerializer

    def post(self, request):
        """
        Overide the default post()
        """

        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        serializer.validate_member(request_data['route'],
                                   request.user.id)
        serializer.is_valid(raise_exception=True)
        serializer.save(member=request.user)

        return_message = {'message': JOINED_ROUTE_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)


class RoutesRetrieveApiView(viewsets.ReadOnlyModelViewSet):
    """
    retrieve: Return Routes.
    list: Return a list of routes
    """
    permission_classes = (IsAuthenticated,)
    queryset = Route.objects.all().order_by('created_at')
    serializer_class = RouteRetrieveSerializer
    pagination_class = Pagination
    filter_backends = (SearchFilter,)
    search_fields = ('commuting_time')

    @action(methods=['GET'], detail=False, url_name='Search users')
    def search(self, request, *args, **kwargs):
        """
        Search users
        """
        return super().list(request, *args, **kwargs)


class RouteRetrieveApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = RouteUpdateSerializer

    def get(self, request, route_id):
        """
        Retrieve route details from the provided
        """
        self.serializer_class = RouteRetrieveSerializer
        route = validate_route_id(route_id)
        serializer = self.serializer_class(route)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, route_id):
        """
        overide the default patch() method to enable
        the user add a vehicle
        """

        self.serializer_class = RouteUpdateSerializer
        route = validate_route_id(route_id)


        data = request.data
        serializer = self.serializer_class(
            route, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
