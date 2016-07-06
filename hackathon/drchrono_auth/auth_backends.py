from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class PasswordlessAuthBackend(ModelBackend):
    """
    Log in to Django without providing a password.
    This backend is meant for API client apps
    which support auth via OAuth2

    """
    # TODO: replace with a less prone to security issues

    def authenticate(self, username=None, token=None):
        # token is meant to make sure that the
        # calling code wanted to use this backend
        if token is None:
            return None
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
