from rest_framework.views import status
from app.api.helpers.constants import JOINED_ROUTE_SUCCESS_MESSAGE
from .base_test import TestBaseCase


class JoinRouteTest(TestBaseCase):

    def test_join_route_successeds(self):
        """
        Test schedule route
        """
        response = self.join_route_successfully()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                        JOINED_ROUTE_SUCCESS_MESSAGE)

    def test_join_route_you_have_joined_fails(self):
        """
        Test schedule route
        """
        response = self.join_route_you_have_joined_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn(
                        b'You are in the route already', response.content)
