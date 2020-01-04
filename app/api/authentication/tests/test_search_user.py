from unittest.mock import patch, Mock
from rest_framework import status
from .base_test import TestBaseCase
from django.urls import reverse


class SearchUserTest(TestBaseCase):
    """
    Test user search and retrieve
    """
    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    def test_search_user_succeeds(self):
        """
        Test search user details successfully
        """
        user = self.activated_user()
        url = reverse("authentication:users-retrieve-search")
        url = url + f'?search=jane&page=1&limit=1'
        response = self.client.get(
            url, HTTP_AUTHORIZATION='Token ' + user.token)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['paginationMeta']['currentPage'], 1)
        self.assertIsInstance(data['paginationMeta'], dict)
        self.assertIsInstance(data['rows'], list)

    @patch('app.api.authentication.views.send_mail_', Mock(return_value=True))
    def test_retrieve_users_succeeds(self):
        """
        Test retrieve all details successfully
        """
        user = self.activated_user()
        url = reverse("authentication:users-retrieve-search")
        response = self.client.get(
            url, HTTP_AUTHORIZATION='Token ' + user.token)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['paginationMeta']['currentPage'], 1)
        self.assertIsInstance(data['paginationMeta'], dict)
        self.assertIsInstance(data['rows'], list)
