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

    def signup_user(self):
        """
        Signup user successfully
        """
        response = self.client.post(
            self.signup_url, self.valid_user, format='json')

        return response
        # return User.objects.get(email=self.valid_user['email'])