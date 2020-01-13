from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from ...authentication.models import User


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.schedule_route_url = api_reverse('route:schedule-route')
        self.login_url = api_reverse('authentication:user-login')

        self.user_one = User.objects.create_user(
            first_name='jane1',
            last_name='Doe1',
            surname='jDoe1',
            email='jane1@doe.com',
            password='janeDoe@123',
            id_number=1223,
            phone_number="+254712534545",
            is_active=True)

        self.user_two = User.objects.create_user(
            first_name='rose',
            last_name='mary',
            surname='mary',
            email='mary@mary.com',
            username="rosemary",
            password='janeDoe@123',
            id_number=122843,
            phone_number="+2547129743545",
            is_active=True)

        self.user_three = User.objects.create_user(
            first_name='Three',
            last_name='Mine',
            surname='James',
            email='user@three.com',
            username="Three",
            password='janeDoe@123',
            id_number=1228444,
            phone_number="+2547179743545",
            is_active=True)

        self.valid_route_details = {
            "destination": {"latitude": 37.0625,"longitude": -95.677068},
            "starting_point":  {"latitude": 37.0625,"longitude": -95.677068},
            "commuting_time": "17:00"
        }

        self.valid_user_login_details = {
                'email': 'jane1@doe.com',
                'password': 'janeDoe@123',
        }
        self.valid_user_two_login_details = {
                'email': 'mary@mary.com',
                'password': 'janeDoe@123',
        }
        self.token = self.login_user().data['token']
        self.token_two = self.login_user_two().data['token']


    def login_user(self):
        """
        method to login user
        """
        return self.client.post(self.login_url,
                                self.valid_user_login_details, format='json')

    def login_user_two(self):
        """
        method to login user
        """
        return self.client.post(self.login_url,
                                self.valid_user_two_login_details, format='json')


    def schedule_route_successfully(self):
        """
        Schedule route successfully
        """
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    def schedule_second_route_fails(self):
        """
        Schedule second route fails
        """
        self.schedule_route_successfully()
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    def schedule_route_without_token_fails(self):
        """
        Schedule route without token fails
        """
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json')

        return response

    def schedule_existing_route_fails(self):
        """
        Schedule an existing route fails
        """
        self.schedule_route_successfully()
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response
