from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from ...authentication.models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.login_url = api_reverse('authentication:user-login')
        self.register_vehicle_url = api_reverse('vehicle:register-vehicle')


        self.user_one = User.objects.create_user(
            first_name='jane1',
            last_name='Doe1',
            surname='jDoe1',
            email='jane1@doe.com',
            password='janeDoe@123',
            id_number=1223,
            phone_number="+254712534545",
            is_active=True)


        self.valid_vehicle_details = {
            "registration_number": "KAC234D",
            "capacity": "20"
        }

        self.valid_user_login_details = {
                'email': 'jane1@doe.com',
                'password': 'janeDoe@123',
        }

        self.token = self.login_user().data['token']


    def login_user(self):
        """
        method to login user
        """
        return self.client.post(self.login_url,
                                self.valid_user_login_details, format='json')

    def register_vehicle_succeeds(self):
        """
        Register vehicle succeeds
        """
        response = self.client.post(
            self.register_vehicle_url, self.valid_vehicle_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response
