from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.urls import reverse


class UserManager(BaseUserManager):
    
    def create_user(self, name, username, email, password = None):
        if username is None:
            raise TypeError('user must have username') 
        if name is None:
            raise TypeError('user must have name')
        if email is None:
            raise TypeError('user must have email')
        user = self.model(username = username,
                          name = name,
                          email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('User Full Name'), max_length=155)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(_('Username'), max_length=155, unique=True)
    is_verified = models.BooleanField(_('Is user verified by email'), default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']
    
    objects = UserManager()

    def get_absolute_url(self):
        """Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username 