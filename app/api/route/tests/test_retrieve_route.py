from rest_framework.views import status
from .base_test import TestBaseCase


class RouteRetrieveTest(TestBaseCase):

    def test_retrieve_route_succeeds(self):
        """
        Test retrieve routes
        """
        response = self.retrieve_route_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertTrue(len(response.data)!=0)

    def test_retrieve_not_existing_route_succeeds(self):
        """
        Test retrieve non existing route
        """
        response = self.retrieve_non_existing_route_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

