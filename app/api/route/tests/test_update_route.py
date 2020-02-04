from rest_framework.views import status
from .base_test import TestBaseCase


class RouteUpdateTest(TestBaseCase):

    def test_add_vehicle_to_route_succeeds(self):
        """
        Test retrieve routes
        """
        response = self.add_vehicle_for_the_route_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(len(response.data)!=0)
