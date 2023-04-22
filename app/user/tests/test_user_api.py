"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create') # user:create => app:endpoint
print("THIS IS THE URL " + str(CREATE_USER_URL))

# Define a helper function to create a user for testing
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

"""
We have two different test classes as follows:
  Public tests - Don't require authentication
    e.g. registering a new user
  Private tests - require authentication
"""
class PublicUserApiTests(TestCase):
  """Test the public features of the user API."""

  def setUp(self):
    # Create an API client that we cna user for testing.
    self.client = APIClient

  def test_create_user_success(self):
    """Test creating a user is successful."""
    # define dictionary with the test payload that we post to the api to
    # test creating a new user
    payload = {
      'email': 'test@example.com',
      'password': 'testpass123',
      'name': 'Test Name',
    }

    # Make POST request to create a user passing in the payload dict
    res = self.client.post(CREATE_USER_URL, payload)

    # status code 201 is the repsone code for creating objects in the
    # database via an API.
    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(email=payload['email'])
    self.assertTrue(user.check_password(payload['password']))

    # we make sure the password hash is not sent back to the user.
    self.assertNotIn('password', res.data)

  def test_user_with_email_exists_error(self):
    """Test error returned if user with email already exists."""
    payload = {
      'email': 'test@example.com',
      'password': 'testpass123',
      'name': 'Test Name',
    }
    # create user with the details defined in the paylaod params.
    create_user(**payload)
    # make the POST rewuest
    res = self.client.post(CREATE_USER_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_password_too_short_error(self):
    """Error returned if password length is fewer than five chars"""
    payload = {
      'email': "test@example.com",
      'password': 'pw',
      'name': "Test Name",
    }

    # Post a registration payload with a password that is too short
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    # Also we ensure that this bad request does not create a user in the
    # database.
    user_exists = get_user_model().objects.filter(
      email=payload['email']
    ).exists()
    # exists() returns a boolean showing whether the query exists
    # confirm user doens't exist in the database
    self.assertFalse(user_exists)
