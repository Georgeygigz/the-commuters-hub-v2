from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.signup_url = api_reverse('authentication:user-registration')

        self.valid_user = {
            'first_name': 'mary',
            'last_name': 'mary',
            'surname': 'mary',
            'username': 'mary',
            'email': 'mm@mm.com',
            'password': 'Pass@123',
            'id_number': 123,
            'phone_number': "+25412534545"
        }

        self.valid_existing_user = {
            'first_name': '1mary',
            'last_name': 'm1ary',
            'surname': 'ma1ry',
            'username': 'ma1ry',
            'email': 'mm@mm.com',
            'password': 'Pass@123',
            'id_number': 1231,
            'phone_number': "+254121534545"
        }

        self.invalid_user_with_missing_fields = {
            'last_name': 'mary',
            'surname': 'mary',
            'username': 'mary',
            'email': 'mm@mm.com',
            'password': 'Pass@123',
            'id_number': 123,
            'phone_number': "+25412534545"
        }

        self.invalid_user_with_empty_fields = {
            'first_name': '',
            'last_name': 'mary',
            'surname': 'mary',
            'username': 'mary',
            'email': 'mm@mm.com',
            'password': 'Pass@123',
            'id_number': 123,
            'phone_number': "+25412534545"
        }

    def signup_user(self):
        """
        Signup user successfully
        """
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')

        return response

    def signup_user_with_missing_fields(self):
        """
        Signup user with missing fields
        """
        response = self.client.post(
            self.signup_url, self.invalid_user_with_missing_fields, format='json')

        return response

    def signup_user_with_empty_fields(self):
        """
        Signup user with empty fields
        """
        response = self.client.post(
            self.signup_url, self.invalid_user_with_empty_fields, format='json')

        return response

    def signup_existing_user(self):
        """
        Signup existing user
        """
        self.signup_user()
        response = self.client.post(
            self.signup_url, self.valid_existing_user, format='json')

        return response
