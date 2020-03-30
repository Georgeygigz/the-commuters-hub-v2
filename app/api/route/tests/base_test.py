from rest_framework.test import APITestCase
import json
from unittest.mock import patch,Mock
from rest_framework.reverse import reverse as api_reverse
from ...authentication.models import User
from ..models import Route
from ...vehicle.models import Vehicle

class TestBaseCase(APITestCase):
    def setUp(self):
        """
        Method for setting up user
        """
        self.schedule_route_url = api_reverse('route:schedule-route')
        self.login_url = api_reverse('authentication:user-login')
        self.join_route_url = api_reverse('route:join-route')
        self.retrieve_route_url = api_reverse('route:retrieve-route')
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
        self.valid_route_two_details = {
            "destination": {"latitude": 31.0625,"longitude": -95.677068},
            "starting_point":  {"latitude": 31.0625,"longitude": -95.677068},
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
        self.valid_user_three_login_details = {
            'email': 'user@three.com',
            'password': 'janeDoe@123',
        }
        self.token = self.login_user().data['token']
        self.token_two = self.login_user_two().data['token']
        self.token_three = self.login_user_three().data['token']
        self.route ={
            'route':self.get_route_object().id
        }

        self.valid_vehicle_details = {
            "registration_number": "KAC236Q",
            "capacity": "5"
        }
        vehicle = self.register_vehicle()
        self.vehicle_id = {
            'vehicle': vehicle.id
        }


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

    def login_user_three(self):
        """
        method to login user
        """
        return self.client.post(self.login_url,
                                self.valid_user_three_login_details, format='json')

    def get_route_object(self):
        self.schedule_route_successfully_two()
        return Route.objects.get(created_by=User.objects.get(email=self.user_three.email).id)

    @patch("requests.get")
    def schedule_route_successfully(self, mock_obj):
        """
        Schedule route successfully
        """
        location_data ={
            "results": [{"geometry":{
            "location": {"lat": -1.2920659, "lng": 36.8219462}},
            "formatted_address":'Nairobi, Kenya'}]}
        return_mock = Mock()
        return_mock.status_code = 200
        return_mock.content = json.dumps(location_data).encode()
        mock_obj.return_value = return_mock

        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    @patch("requests.get")
    def schedule_route_successfully_two(self,mock_obj):
        """
        Schedule route successfully
        """
        location_data ={
            "results": [{"geometry":{
            "location": {"lat": -1.2920659, "lng": 36.8219462}},
            "formatted_address":'Nairobi, Kenya'}]}
        return_mock = Mock()
        return_mock.status_code = 200
        return_mock.content = json.dumps(location_data).encode()
        mock_obj.return_value = return_mock

        response = self.client.post(
            self.schedule_route_url, self.valid_route_two_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_three))

        return response

    @patch("requests.get")
    def schedule_second_route_fails(self,mock_obj):
        """
        Schedule second route fails
        """
        location_data ={
            "results": [{"geometry":{
            "location": {"lat": -1.2920659, "lng": 36.8219462}},
            "formatted_address":'Nairobi, Kenya'}]}
        return_mock = Mock()
        return_mock.status_code = 200
        return_mock.content = json.dumps(location_data).encode()
        mock_obj.return_value = return_mock
        self.schedule_route_successfully()
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token))

        return response

    @patch("requests.get")
    def schedule_route_without_token_fails(self, mock_obj):
        """
        Schedule route without token fails
        """
        location_data ={
            "results": [{"geometry":{
            "location": {"lat": -1.2920659, "lng": 36.8219462}},
            "formatted_address":'Nairobi, Kenya'}]}
        return_mock = Mock()
        return_mock.status_code = 200
        return_mock.content = json.dumps(location_data).encode()
        mock_obj.return_value = return_mock
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json')

        return response

    @patch("requests.get")
    def schedule_existing_route_fails(self, mock_obj):
        """
        Schedule an existing route fails
        """
        location_data ={
            "results": [{"geometry":{
            "location": {"lat": -1.2920659, "lng": 36.8219462}},
            "formatted_address":'Nairobi, Kenya'}]}
        return_mock = Mock()
        return_mock.status_code = 200
        return_mock.content = json.dumps(location_data).encode()
        mock_obj.return_value = return_mock
        self.schedule_route_successfully()
        response = self.client.post(
            self.schedule_route_url, self.valid_route_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response

    def join_route_successfully(self):
        """
        Schedule an existing route fails
        """
        response = self.client.post(
            self.join_route_url, self.route, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response

    def join_route_you_have_joined_fails(self):
        """
        Schedule an existing route fails
        """
        self.join_route_successfully()
        response = self.client.post(
            self.join_route_url, self.route, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response

    def retrieve_routes_successfully (self):
        """
        Retrieve all routes
        """
        self.schedule_route_successfully()
        response = self.client.get(
            self.retrieve_route_url, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response

    def retrieve_route_successfully (self):
        """
        Retrieve single route
        """
        self.register_vehicle()
        route = self.get_route_object()
        response = self.client.get(
            api_reverse('route:route', args=[route.id]),
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response

    def retrieve_non_existing_route_fails (self):
        """
        Retrieve single route
        """
        self.register_vehicle()
        response = self.client.get(
            api_reverse('route:route', args=['-LaAAScbw94sd']),
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return response


    def register_vehicle(self):
        self.client.post(
            self.register_vehicle_url, self.valid_vehicle_details, format='json',
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))

        return Vehicle.objects.filter(owner=self.user_two.id).first()


    def add_vehicle_for_the_route_successfully(self):
        """
        Add vehicle for the route successfully
        """
        route = self.get_route_object()
        response = self.client.patch(
            api_reverse('route:route', args=[route.id]),
            self.vehicle_id ,
            HTTP_AUTHORIZATION='token {}'.format(self.token_two))
        return response

