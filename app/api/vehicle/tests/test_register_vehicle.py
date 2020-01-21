from rest_framework.views import status
from app.api.helpers.constants import (VEHICLE_REGISTRATION_SUCCESS_MESSAGE)
from .base_test import TestBaseCase


class RegisterVehicleTest(TestBaseCase):

    def test_register_vehicle_successeds(self):
        """
        Test schedule route
        """
        response = self.register_vehicle_succeeds()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                        VEHICLE_REGISTRATION_SUCCESS_MESSAGE)
