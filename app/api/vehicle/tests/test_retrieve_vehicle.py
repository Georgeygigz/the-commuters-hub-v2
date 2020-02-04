from rest_framework.views import status
from .base_test import TestBaseCase


class VehicleRetrieveTest(TestBaseCase):

    def test_retrieve_vehicle_succeeds(self):
        """
        Test vehicle routes
        """
        response = self.retrieve_vehicle_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(len(response.data)!=0)

    def test_retrieve_non_existing_vehicle_fails(self):
        """
        Test vehicle routes
        """
        response = self.retrieve_non_existing_vehicle_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_vehicle_without_token_fails(self):
        """
        Test vehicle retrieve vehicle without token
        """
        response = self.retrieve_vehicle_without_token()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            b'Authentication credentials were not provided', response.content)

    def test_retrieve_vehicles_successfully(self):
        """
        Test retrieve vehicles successfully
        """
        response = self.retrieve_vehicles()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['paginationMeta']['currentPage'], 1)
        self.assertIsInstance(response.data['paginationMeta'], dict)
        self.assertIsInstance(response.data['rows'], list)

