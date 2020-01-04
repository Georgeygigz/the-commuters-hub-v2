from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from ..models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.signup_url = api_reverse('authentication:user-registration')
        self.login_url = api_reverse('authentication:user-login')
        self.retrieve_update_user_url = api_reverse(
            'authentication:user-retrieve-update')

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

        self.user_two = User.objects.create_user(
            first_name='jane1',
            last_name='Doe1',
            surname='jDoe1',
            email='jane1@doe.com',
            password='janeDoe@123',
            id_number=1223,
            phone_number="+254712534545",
            is_active=True)

        self.valid_user_login_details = {
            'email': 'jane1@doe.com',
            'password': 'janeDoe@123'
        }

        self.invalid_user_login_details = {
            'email': 'janee@doe.com',
            'password': 'janeDoe@123'
        }

        self.valid_user_two = {
            'username': 'Doe123',
            'password': 'Jan5432@123',
        }

    def signup_user(self):
        """
        Signup user successfully
        """
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')

        return response

    def signup_user_two(self):
        """
        successfully signup user
        """
        self.client.post(
            self.signup_url, self.valid_user, format='json')
        return User.objects.get(email=self.valid_user['email'])

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

    def login_user_successfull(self):
        """
        method to login user
        """
        response = self.client.post(self.login_url,
                                    self.valid_user_login_details, format='json')
        return response

    def login_user_fails(self):
        """
        method to try login a user with invalid data
        """
        response = self.client.post(self.login_url,
                                    self.invalid_user_login_details, format='json')
        return response

    def activated_user(self):
        """
        create an active user
        """
        user = self.signup_user_two()
        user.is_active = True
        user.save()
        return user
