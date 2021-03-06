from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        respons = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(respons.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**respons.data)
        self.assertTrue(user.chec_password(payload['password']))
        self.assertNotIn('password', respons.data)
    
    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@test.com', 'password':'testpass'}
        create_user(**payload)

        respons = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(respons.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Test that the password must be more than 5 characters."""
        payload = {'email': 'test@test.com', 'password':'aa'}
        respons = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(respons.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email = payload['email']).exists()
        self.assertFalse(user_exists)
        