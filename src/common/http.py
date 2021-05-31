from django.http import JsonResponse
from rest_framework import status as _status
from rest_framework.response import Response as _Response

status = _status


class Response(_Response):
    pass


class DjangoJsonResponse(JsonResponse):
    pass
