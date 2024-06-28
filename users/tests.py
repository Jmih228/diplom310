from rest_framework.test import (APITestCase,
                                 APIClient)
from rest_framework import status
from users.models import CustomUser


class UsersServiceTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email='user@sky.pro',
                                              password='hghghg777',
                                              phone_number='+79281337228',)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_register(self):

        data = {
            'email': 'user@mail.ru',
            'password': 'hghghg777',
            'phone_number': '+79283228111'
        }

        response = self.client.post(
            '/users/register/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 4, 'email': 'user@mail.ru', 'phone_number': '+79283228111',
             'city': None, 'invite_code': None, 'invited_users': ['+79281337228', '+79283228111']})

    def test_get_sms_code(self):

        data = {'phone_number': self.user.phone_number}

        response = self.client.post(
            '/users/get_sms_code/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_profile(self):

        response = self.client.get(
            '/users/profile/',
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': 5, 'email': 'user@sky.pro', 'phone_number': '+79281337228',
              'city': None, 'invite_code': None, 'invited_users': ['+79281337228']}])

    def test_profile_update(self):

        data = {'city': 'update'}

        response = self.client.patch(
            f'/users/profile_update/{self.user.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'email': 'user@sky.pro', 'phone_number': '+79281337228', 'city': 'update',
             'invite_code': None, 'invited_users': ['+79281337228']}
        )
