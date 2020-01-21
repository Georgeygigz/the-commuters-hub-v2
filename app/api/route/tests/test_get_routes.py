from rest_framework.views import status
from .base_test import TestBaseCase


class RouteRetrieveTest(TestBaseCase):

    def test_retrieve_routes_succeeds(self):
        """
        Test retrieve routes
        """
        response = self.retrieve_routes_successfully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data['paginationMeta']['currentPage'], 1)
        self.assertIsInstance(response.data['paginationMeta'], dict)
        self.assertIsInstance(response.data['rows'], list)
