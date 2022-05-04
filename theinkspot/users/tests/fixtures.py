import pytest


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
        user_data["password"] = "password"
        user_data["name"] = "admin_name"  # TODO this is the fix
        user_data[username_field] = username
        user = UserModel._default_manager.create_superuser(**user_data)
    return user
