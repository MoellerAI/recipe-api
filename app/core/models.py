from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password = None, **extra_fields):
        """Creates and saves a new Suser.
        
        Args:
            email [str]: Email-address for user.
            password [str, optional]: password related to user. will be encrypted.
            extra_fields: any additional fields related to the BaseUserManager from Django.
        
        Returns:
            user: Django user. 
        """
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(max_length=255,unique = True) # user needs to be unique by email.
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # user is set as active when created.
    is_staff = models.BooleanField(default=False) # users are not staff when created (superusers).

    objects = UserManager()
    
    USERNAME_FIELD = 'email'