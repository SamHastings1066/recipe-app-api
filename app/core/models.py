"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


# Define the UserManager class inheriting from the BaseUserManager class
# from Django
class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Creat, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        # Our manager is associated to a model. The self.model syntax allows
        # us to access the model we're associated with. The is the same as
        # defining a new user out of our user class.
        # the normalize_email method is provided by the BaseUserManager
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # the set_password method sets an encrypted password. Using a hashing
        # function.
        user.set_password(password)
        # Save the user model - using-self._db supports using multiple
        # databases.
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# AbstractBaseUser contains the functionality for the authentication system
# but not fields; PermissionsMixin contains the functionality for django's
# permissions feature as well as the fields that are needed for that feature.
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign this user manager to our custom User class
    objects=UserManager()

    USERNAME_FIELD = 'email'
