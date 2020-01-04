from unittest.mock import patch,Mock
from rest_framework import status
from .base_test import TestBaseCase


class RetrieveUserTest(TestBaseCase):
    """
    Test for account verification
    """
    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    def test_retrieve_user_succeeds(self):
        """
        Test retrieve user details successfully
        """
        user = self.activated_user()
        response = self.client.get(
            self.retrieve_update_user_url, HTTP_AUTHORIZATION='Token ' + user.token)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['first_name'], user.first_name)
        self.assertEqual(data['last_name'], user.last_name)
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['phone_number'], user.phone_number)

    def test_retrieve_user_without_token_fails(self):
        """
        Test for user retrieval failure
        due to missing token
        """
        response = self.client.get(self.retrieve_update_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            b'Authentication credentials were not provided.', response.content)
