import logging
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json
from booksapp.models import User
from booksapp.factories import UserFactory


class TestUserSignUp(APITestCase):

    def test_it_fails_to_create_account_given_invalid_data(self):
        url = reverse('register')
        data = {'first_name': 'lawrence'}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_it_creates_account_given_valid_data(self):
        url = reverse('register')
        data = {'first_name': 'lawrence',
                'last_name': 'arkoh',
                'username': 'k@gmail.com',
                'email': 'k@gmail.com',
                'password': 'tes@82dsk'}

        response = self.client.post(url, data, format='json')
        response_data = json.loads(response.content)
        self.assertTrue(User.objects.filter(email=data['email']).exists())
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response_data['message'], 'user created successfully.')

    def test_it_login_successfullly_given_valid_credentials(self):
        user = UserFactory()
        url = reverse('login')
        data = {
            'username': user.email,
            'password': 'password'}

        response = self.client.post(url, data, format='json')
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
