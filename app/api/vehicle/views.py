from rest_framework import status
from rest_framework import generics,mixins
from rest_framework.response import Response
from ..helpers.renderers import RequestJSONRenderer
from rest_framework.permissions import IsAuthenticated
from .serializers import (VehicleRegistrationSerializer,
                          VehicleUpdateSerializer,
                          VehicleRetrieveSerializer)
from ..helpers.constants import VEHICLE_REGISTRATION_SUCCESS_MESSAGE
from .validators.validate_vehicle import validate_vehicle_id


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


class VehicleRetrieveUpdateApiView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (RequestJSONRenderer,)
    serializer_class = VehicleRetrieveSerializer

    def get(self, request, vehicle_id):
        """
        Retrieve vehicle details from the provided
        """
        vehicle = validate_vehicle_id(request.user.id, vehicle_id)
        serializer = self.serializer_class(vehicle)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, vehicle_id):
        """
        overide the default patch() method to enable
        the user add a vehicle
        """
        self.serializer_class = VehicleUpdateSerializer
        vehicle = validate_vehicle_id(request.user.id, vehicle_id)

        data = request.data
        serializer = self.serializer_class(
            vehicle, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
