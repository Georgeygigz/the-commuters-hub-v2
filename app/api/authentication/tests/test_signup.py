from rest_framework import status
from .base_test import TestBaseCase
from ...helpers.constants import SIGNUP_SUCCESS_MESSAGE
from ...helpers.serialization_errors import error_dict


class AuthenticationTest(TestBaseCase):
    """
    User signup test cases
    """

    def test_user_signup_succeed(self):
        """
        Test API can successfully register a new user
        """
        response = self.signup_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], SIGNUP_SUCCESS_MESSAGE)