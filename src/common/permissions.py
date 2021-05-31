from rest_framework import permissions as _permissions


class AllowAny(_permissions.AllowAny):
    pass


class IsAdminUser(_permissions.IsAdminUser):
    pass


class IsAuthenticated(_permissions.IsAuthenticated):
    pass


class BasePermission(_permissions.BasePermission):
    pass
