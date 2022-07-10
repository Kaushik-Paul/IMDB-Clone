from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@test.com",
            "password": "test",
            "password2": "test"
        }
        response = self.client.post(reverse('register'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="example",
            password="test",
            email="testuser@test.com",
        )

        print(str(self.user.username))

    def test_login(self):
        data = {
            'username': "example",
            'password': 'test'
        }

        response = self.client.post(reverse('login'), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        user = User.objects.get(username='example')
        self.token = Token.objects.get(user=user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
