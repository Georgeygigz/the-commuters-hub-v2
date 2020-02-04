from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework.reverse import reverse as api_reverse
from ...authentication.models import User
from ..models import Vehicle


class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.login_url = api_reverse('authentication:user-login')
        self.register_vehicle_url = api_reverse('vehicle:register-vehicle')
        self.retrieve_vehicles_url = api_reverse('vehicle:vehicle-retrieve')


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
            first_name='jane1',
            last_name='Doe1',
            surname='jDoe1',
            email='mary@mary.com',
            password='Pass@123',
            username="mary",
            id_number=12233,
            phone_number="+2547125334545",
            is_active=True)


        self.valid_vehicle_details = {
            "registration_number": "KAC234D",
            "capacity": "20"
        }

        self.valid_user_login_details = {
                'email': "jane1@doe.com",
                'password': "janeDoe@123",
        }

        self.valid_user_two_login_details = {
                'email': "mary@mary.com",
                'password': "Pass@123",
        }

        self.token = self.login_user().data['token']
        self.token_two = self.login_user_two().data['token']
        self.fare = {
            "fare":200
        }


    def login_user(self):
        """
        method to login user
        """
        return self.client.post(self.login_url,
                                self.valid_user_login_details, format='json')
    def login_user_two(self):
        """
        method to login user two
        """
        return self.client.post(self.login_url,
                                self.valid_user_two_login_details, format='json')

    def register_vehicle_succeeds(self):
        """
        Register vehicle succeeds
        """
        response = self.client.post(
            self.register_vehicle_url, self.valid_vehicle_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response

    def register_vehicle(self):
        self.client.post(
        self.register_vehicle_url, self.valid_vehicle_details, format='json',
        HTTP_AUTHORIZATION='token {}'.format(self.token))

        return Vehicle.objects.filter(owner=self.user_one.id).first()

    def retrieve_vehicle_successfully (self):
        """
        Retrieve single vehicle
        """
        self.register_vehicle()
        vehicle = self.register_vehicle()
        response = self.client.get(
            reverse('vehicle:update-fare', args=[vehicle.id]),
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    def retrieve_vehicle_without_token (self):
        """
        Retrieve single vehicle without token
        """
        vehicle = self.register_vehicle()
        response = self.client.get(
            reverse('vehicle:update-fare', args=[vehicle.id]))

        return response

    def retrieve_non_existing_vehicle_fails (self):
        """
        Retrieve non existing vehicle
        """
        self.register_vehicle()
        response = self.client.get(
            reverse('vehicle:update-fare', args=['-Lklsndw834jk8wke']),
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    def update_vehicle_fare_successfully(self):
        """
        Update vehicle fare successfully
        """
        vehicle = self.register_vehicle()
        response = self.client.patch(
            reverse('vehicle:update-fare', args=[vehicle.id]),
            self.fare ,
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response

    def update_vehicle_fare_no_rights(self):
        """
        Update vehicle fare with no rights
        """
        vehicle = self.register_vehicle()
        response = self.client.patch(
            reverse('vehicle:update-fare', args=[vehicle.id]),
            self.fare ,
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))
        return response

    def update_non_existing_vehicle_fails(self):
        """
        Update non existing vehicle fails
        """
        response = self.client.patch(
            reverse('vehicle:update-fare', args=['-LsaKac4wduiew']),
            self.fare ,
            HTTP_AUTHORIZATION='token {}'.format(self.token))
        return response

    def retrieve_vehicles (self):
        """
        Retrieve  vehicles
        """
        self.register_vehicle()
        response = self.client.get(
                self.retrieve_vehicles_url, format='json',
                HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response
