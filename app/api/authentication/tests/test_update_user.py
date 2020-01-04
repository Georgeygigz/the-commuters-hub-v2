from unittest.mock import patch,Mock
from rest_framework import status
from .base_test import TestBaseCase
from ..models import User


class UpdateUserTest(TestBaseCase):
    """
    Update user test case
    """
    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    def test_user_update_succeed(self):
        """
        Test API can successfully update user details
        """
        user = self.activated_user()
        response = self.client.patch(
            self.retrieve_update_user_url, self.valid_user_two, format='json', HTTP_AUTHORIZATION='Token ' + user.token)
        user_ = User.objects.get(email=user.email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_.username, self.valid_user_two['username'])
