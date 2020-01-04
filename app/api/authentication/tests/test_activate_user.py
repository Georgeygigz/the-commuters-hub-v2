from unittest.mock import patch, Mock
from django.urls import reverse
from rest_framework import status
from .base_test import TestBaseCase
from ..models import User


class ActivateUserTest(TestBaseCase):
    """
    Activate user test cases
    """
    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    def test_activate_user_succeeds(self):
        """
        Test for successful account verification
        """
        user = self.signup_user_two()
        response = self.client.get(
            reverse("authentication:user-verify", args=[user.token]))
        user = User.objects.get(id=user.id)
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
