from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model


class PublicAuthMiddleware(MiddlewareMixin):
    """
        Helps to skip authentication.
    """

    def process_request(self, request):
        request.user, created = get_user_model().objects.get_or_create(is_staff=True, is_superuser=True)
