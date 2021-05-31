from django.db import connection
from rest_framework.generics import get_object_or_404 as _get_object_or_404
from rest_framework.views import APIView as DRFView

from common.http import Response, status
from common.permissions import AllowAny

get_object_or_404 = _get_object_or_404


class APIView(DRFView):
    pass


class HealthView(DRFView):
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):     # noqa
        try:
            connection.ensure_connection()
            return Response(
                status=status.HTTP_200_OK,
                data={'status': 'ok'},
            )
        except Exception as e:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'status': 'error', 'detail': str(e)},
            )
