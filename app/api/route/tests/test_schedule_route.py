import json
from unittest.mock import patch,Mock
from rest_framework.views import status
from app.api.helpers.constants import (REQUEST_SUCCESS_MESSAGE)
from .base_test import TestBaseCase


class ScheduleRouteTest(TestBaseCase):

    @patch("requests.get")
    def test_schedule_route_successeds(self, mock_obj):
        """
        Test schedule route
        """
        location_data ={
            "results": [{"geometry":{
            "location": {"lat": -1.2920659, "lng": 36.8219462}},
            "formatted_address":'Nairobi, Kenya'}]}
        mock_responses = Mock()
        mock_responses.content = json.dumps(location_data).encode()
        mock_obj.side_effect = mock_responses

        response = self.schedule_route_successfully()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn(
            b'A similar route exist already',response.content)

    def test_user_schedule_second_route_fails(self):
        """
        User schedule second route_fails
        """
        response = self.schedule_second_route_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIn(
            b'A similar route exist already',response.content)

    def test_schedule_route_without_token_fails(self):
        """
        User schedule route without token fails
        """
        response = self.schedule_route_without_token_fails()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(json.loads(response.content),
            {'detail': 'Authentication credentials were not provided.', 'status': 'failed'})

    def test_schedule_existing_route_fails(self):
        """
        User schedule existing route_fails
        """
        response = self.schedule_existing_route_fails()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(json.loads(response.content),
            {'errors': ['A similar route exist already'], 'status': 'failed'})
