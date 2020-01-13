from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from ..helpers.renderers import RequestJSONRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import SchedulingRouteSerializer
from ..helpers.constants import REQUEST_SUCCESS_MESSAGE
from .validators.route import validate_route

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

        return_message = {'message': REQUEST_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)
