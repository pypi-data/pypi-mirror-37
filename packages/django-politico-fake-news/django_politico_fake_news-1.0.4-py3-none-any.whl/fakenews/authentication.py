from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework import authentication, exceptions

from fakenews.conf import settings as app_settings


class TokenAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Don't enforce if DEBUG
        if settings.DEBUG:
            return (AnonymousUser, None)

        # Per DRF token auth, token is prefixed by string
        # literal "Token" plus whitespace, e.g., "Token <AUTHTOKEN>"
        token_str = request.META.get('HTTP_AUTHORIZATION')
        if not token_str:
            raise exceptions.AuthenticationFailed(
                'No token or incorrect token format')

        token = token_str.split()[1]

        if token == app_settings.API_TOKEN:
            return (AnonymousUser, None)
        raise exceptions.AuthenticationFailed('Unauthorized')


def secure(view):
    """Set an auth decorator applied for views.
    If DEBUG is on, we serve the view without authenticating.
    Default is 'django.contrib.auth.decorators.login_required'.
    Can also be 'django.contrib.admin.views.decorators.staff_member_required'
    or a custom decorator.
    """
    # Don't enforce if DEBUG
    if settings.DEBUG:
        return (view)

    return method_decorator(
        app_settings.AUTH_DECORATOR, name='dispatch'
    )(view)
