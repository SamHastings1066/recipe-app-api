"""
Tests for the Django admin modifications.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):
    """Tests for Django admin."""
    # setup method allows us to set up some modules to be run before any test
    # we add subsequently

    # N.B. the unit test module expects snakeCase for its methods.
    def setUp(self):
        """Create user and client"""
        # This is teh Django test client that allows us to make http requests
        self.client = Client()
        # we use the create_superuser method of our model manager
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )

        # the force login method allows us to force the authentication to this
        # user. So every request we make to this client is going to be
        # authenticated with this user that we've created
        self.client.force_login(self.admin_user)
        # Create a user we can use to test the listing etc. in the Django admin
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page"""
        # user reverse to get the url for the changelist inside the Django
        # admin. This gets the url for the page that shows the list of
        # users in the system
        url = reverse('admin:core_user_changelist')
        # client.get makes an http request to the url. Because we have used
        # force_login in the setUp the request is made authenticated as
        # user that we forced the login on (the admin user)
        res = self.client.get(url)

        # check that the response object from that url contains name and
        # email address
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # gets the url for core user cahnge - something like:
        # admin/core/user/1/change/
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Ensure the page loads successfully with an http 200 response.
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test to create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
