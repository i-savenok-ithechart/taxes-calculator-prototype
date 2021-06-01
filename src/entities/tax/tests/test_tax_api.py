import pytest
from common.http import status
from project.settings import API_URL_PREFIX

PATH = f'/{API_URL_PREFIX}taxes/'


@pytest.mark.django_db
class TestTaxApi:

    def test_calculate_tax(self, api_client_factory):
        response = api_client_factory().put(
            f'{PATH}?detailed=true&year=2000',
            data={'annual_salary_amount': 200.01},
        )
        assert 1
