from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from ..helpers.renderers import RequestJSONRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import (SchedulingRouteSerializer,
                          MemberSerializer)
from ..helpers.constants import (REQUEST_SUCCESS_MESSAGE,
                                JOINED_ROUTE_SUCCESS_MESSAGE)
from .validators.route import validate_route
from ..helpers.route_members import add_route_member

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


class JoinRouteAPiView(generics.CreateAPIView):
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
