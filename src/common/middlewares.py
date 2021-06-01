from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin


class PublicAuthMiddleware(MiddlewareMixin):
    """
        Helps to skip authentication.
    """

    def process_request(self, request):
        request.user, created = get_user_model().objects.get_or_create(is_staff=True, is_superuser=True)
