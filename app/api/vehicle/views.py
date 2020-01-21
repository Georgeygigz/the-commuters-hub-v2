from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from ..helpers.renderers import RequestJSONRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import VehicleRegistrationSerializer
from ..helpers.constants import VEHICLE_REGISTRATION_SUCCESS_MESSAGE


# Create your views here.
class RegisterVehicleApiView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = VehicleRegistrationSerializer

    def post(self, request):
        """
        Overide the default post()
        """

        request_data = request.data
        serializer = self.serializer_class(data=request_data)

        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return_message = {'message': VEHICLE_REGISTRATION_SUCCESS_MESSAGE}
        return Response(return_message, status=status.HTTP_201_CREATED)

