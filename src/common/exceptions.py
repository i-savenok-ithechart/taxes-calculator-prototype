from django.core.exceptions import ObjectDoesNotExist as DjangoObjectDoesNotEx
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError as DjangoIntegrityError
from django.http import Http404 as DjangoHttp404
from rest_framework import exceptions as _exceptions

from common.http import status

ValidationError = DjangoValidationError
IntegrityError = DjangoIntegrityError
ObjectDoesNotExist = DjangoObjectDoesNotEx
PermissionDenied = DjangoPermissionDenied
Http404 = DjangoHttp404


class DRFValidationError(_exceptions.ValidationError):
    pass


class NotFoundAPIException(_exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = 'error'
    detail = "Not found."


class BadRequestAPIException(_exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'
    detail = "Bad request."


class PermissionDeniedAPIException(_exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'error'
    detail = "Permission denied."


class AuthenticationFailedAPIException(_exceptions.AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'authentication_failed'
    default_detail = 'Incorrect authentication credentials.'


class MethodNotAllowedAPIException(_exceptions.MethodNotAllowed):
    pass
