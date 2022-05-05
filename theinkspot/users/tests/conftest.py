import pytest

from theinkspot.users.models import User

"""
This module will provide fixtures for the entire directory,
Fixtures defined here will be used in any test automatically
without importing them *according to pytest-django documentation*
"""

# modified the admin user fixture to add the "name" field to the user_data
# before passing it the create_superuser function because it is one of the
# required fields in the user model


@pytest.fixture()
def admin_user(
    db: None,
    django_user_model,
    django_username_field: str,
):
    """A Django admin user.
    This uses an existing user with username "admin", or creates a new one with
    password "password".
    """
    UserModel = django_user_model
    username_field = django_username_field
    username = "admin@example.com" if username_field == "email" else "admin"

    try:
        # The default behavior of `get_by_natural_key()` is to look up by `username_field`.
        # However the user model is free to override it with any sort of custom behavior.
        # The Django authentication backend already assumes the lookup is by username,
        # so we can assume so as well.
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        user_data = {}
        if "email" in UserModel.REQUIRED_FIELDS:
            user_data["email"] = "admin@example.com"
        if "name" in UserModel.REQUIRED_FIELDS:
            user_data["name"] = "user full name"
        user_data["password"] = "password"
        user_data[username_field] = username
        user = UserModel._default_manager.create_superuser(**user_data)
    return user


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        name="user name",
        username="username",
        email="test@email.com",
        password="Am0123456789123456",
    )


@pytest.fixture
def superuser(db) -> User:
    return User.objects.create_superuser(
        name="user name",
        username="username",
        email="test@email.com",
        password="Am0123456789123456",
    )
