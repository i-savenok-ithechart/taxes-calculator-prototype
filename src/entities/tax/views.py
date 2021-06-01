from typing import Optional

from common.exceptions import DRFValidationError
from common.http import Request, Response
from common.views import APIView
from entities.tax.models import Tax
from entities.tax.serializers import TaxInputSerializer, TaxOutputSerializer


class TaxView(APIView):
    http_method_names = ('put',)

    def put(self, request: Request, *args, **kwargs):
        serializer = TaxInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        annual_salary_amount = serializer.validated_data.get('annual_salary_amount', 0)
        year = self._get_year_param(request)
        tax = Tax(annual_salary_amount=annual_salary_amount, year=year)

        detailed = self._get_detailed_param(request)
        return Response(data=TaxOutputSerializer(tax=tax, detailed=detailed).data)

    @classmethod
    def _get_year_param(cls, request: Request) -> Optional[int]:
        is_year_provided = 'year' in request.query_params
        if is_year_provided:
            year = request.query_params['year']
            if not str(year).isdigit() or int(year) < 0:
                raise DRFValidationError(detail='The year param must be a positive number', code='invalid')
            return year

    @classmethod
    def _get_detailed_param(cls, request: Request) -> bool:
        is_detailed_provided = 'detailed' in request.query_params
        if is_detailed_provided:
            detailed = {'false': False, 'true': True}.get(request.query_params['detailed'])
            if not detailed:
                raise DRFValidationError(
                    detail='"detailed" param have invalid value, the valid choices are "true" or "false"',
                    code='invalid',
                )
            return detailed
        return False
