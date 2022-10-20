from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

CREATE_USER = reverse('create-user')
CREATE_TOKEN = reverse('token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_create_user_success(self):
        """ test create user successful """
        payload = {'username': 'usernametest', 'password': 'passwordtest'}

        res = self.client.post(CREATE_USER, payload)
        user = get_user_model().objects.get(username=payload['username'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_create_user_exists(self):
        """ test create user with username exists """
        payload = {'username': 'usernametest', 'password': 'passwordtest'}

        create_user(**payload)

        res = self.client.post(CREATE_USER, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_error_password(self):
        """ test create user with short password """
        payload = {'username': 'usernametest', 'password': 'pass'}

        res = self.client.post(CREATE_USER, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_success(self):
        """ test create token with valid credentials """
        payload = {'username': 'usernametest', 'password': 'passwordtest'}

        create_user(**payload)

        res = self.client.post(CREATE_TOKEN, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
    
    def test_create_token_user_not_exists(self):
        """ test create token with user not exists """
        payload = {'username': 'usernametest', 'password': 'testpassword'}
        
        res = self.client.post(CREATE_TOKEN, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)
    
    def test_create_token_invalid(self):
        """ test create token with invalid credentials """
        user = {'username': 'usernametest', 'password': 'passwordtest'}
        payload = {'username': user['username'], 'password': 'passwordtest1'}
        
        create_user(**user)

        res = self.client.post(CREATE_TOKEN, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)
    
    def test_create_token_blank_password(self):
        """ test create token with blanck password """
        user = {'username': 'usernametest', 'password': 'pass'}
        payload = {'username': user['username'], 'password': ''}

        create_user(**user)

        res = self.client.post(CREATE_TOKEN, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', res.data)
    
    