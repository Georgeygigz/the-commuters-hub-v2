# Python and Django imports
from unittest.mock import Mock
from rest_framework.views import status
from ...authentication.tasks import send_mail_
from ...helpers.constants import PASS_RESET_MESSAGE

from .base_test import TestBaseCase


class TestPasswordReset(TestBaseCase):
    """
    Handle password reset tests
    """

    def test_reset_email_sent_successfully(self):
        """
        Test that a password reset email is sent
        to the user
        """
        send_mail_.delay = Mock(return_value=True)
        user = self.activated_user()
        response = self.client.post(self.pass_reset_url,
                                    data={"email": user.email},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            PASS_RESET_MESSAGE, response.data['message'])
        send_mail_.delay.assert_called()

    def test_reset_password_non_existent_mail_fails(self):
        """
        Test that reset password with non existent email
        fails
        """
        response = self.client.post(self.pass_reset_url,
                                    data={"email": "tes@user.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b"The email provided is not registered",
                      response.content)
