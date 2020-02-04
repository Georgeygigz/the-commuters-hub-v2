from rest_framework.views import status
from .base_test import TestBaseCase


class VehicleUpdateTest(TestBaseCase):

    def test_update_vehicle_succeeds(self):
        """
        Test update vehicle
        """
        response = self.update_vehicle_fare_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(len(response.data)!=0)

    def test_update_vehicle_no_access_fails(self):
        """
        Test update vehicle fails
        """
        response = self.update_vehicle_fare_no_rights()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            b'You are not the owner of this vehicle',response.content)

    def test_update_non_existing_vehicle_fails(self):
        """
        Test vehicle routes
        """
        response = self.update_non_existing_vehicle_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

