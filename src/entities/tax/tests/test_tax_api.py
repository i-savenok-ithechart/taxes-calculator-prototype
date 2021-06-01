import pytest

from common.decimal import Decimal
from common.http import status
from common.datetime import get_current_year
from project.settings import API_URL_PREFIX

PATH = f'/{API_URL_PREFIX}taxes/'


@pytest.mark.django_db
class TestTaxApi:

    def test_calculate_tax_1(self, api_client_factory, taxes_policy_with_ranges_factory):
        taxes_policy_with_ranges_factory(year=get_current_year(), ranges_values=[
            (0, 12.500, 0),
            (12.501, 50.000, 20),
            (50.001, 150.000, 40),
            (150.001, None, 45),
        ])
        response = api_client_factory().put(f'{PATH}', data={'annual_salary_amount': 52.000})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'annual_salary_amount': '52.0000',
            'year': str(get_current_year()),
            'total_tax_amount': '8.2994',
        }

        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': 52.000})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'annual_salary_amount': '52.0000',
            'year': str(get_current_year()),
            'total_tax_amount': '8.2994',
            'details': [
                {'amount_from': '0.0000', 'amount_to': '12.5000', 'percent': '0', 'tax_amount': '0.0000'},
                {'amount_from': '12.5010', 'amount_to': '50.0000', 'percent': '20', 'tax_amount': '7.4998'},
                {'amount_from': '50.0010', 'amount_to': '150.0000', 'percent': '40', 'tax_amount': '0.7996'},
                {'amount_from': '150.0010', 'amount_to': '*', 'percent': '45', 'tax_amount': '0.0000'}
            ]
        }

    def test_calculate_tax_2(self, api_client_factory, taxes_policy_with_ranges_factory):
        taxes_policy_with_ranges_factory(year=get_current_year(), ranges_values=[
            (10, 15, 10),
            (16, 30, 20),
            (31, None, 50),
        ])
        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': 100.000})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'annual_salary_amount': '100.0000',
            'year': '2021',
            'total_tax_amount': '37.8000',
            'details': [
                {'amount_from': '10.0000', 'amount_to': '15.0000', 'percent': '10', 'tax_amount': '0.5000'},
                {'amount_from': '16.0000', 'amount_to': '30.0000', 'percent': '20', 'tax_amount': '2.8000'},
                {'amount_from': '31.0000', 'amount_to': '*', 'percent': '50', 'tax_amount': '34.5000'}
            ]
        }

    def test_calculate_tax_if_police_have_not_any_ranges(self, api_client_factory, taxes_policy_with_ranges_factory):
        taxes_policy_with_ranges_factory(year=get_current_year(), ranges_values=[])
        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': 52.000})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'annual_salary_amount': '52.0000',
            'year': str(get_current_year()),
            'total_tax_amount': '0.0000',
            'details': []
        }

    def test_calculate_tax_while_no_polices_stored(self, api_client_factory):
        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': 50.000})
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.json()['total_tax_amount']) > 0

    def test_calculate_tax_for_special_year(self, api_client_factory, taxes_policy_with_ranges_factory):
        year = 2020
        taxes_policy_with_ranges_factory(year=year-1, ranges_values=[(0, None, 0)])
        taxes_policy_with_ranges_factory(year=year, ranges_values=[(0, None, 100)])
        taxes_policy_with_ranges_factory(year=year+1, ranges_values=[(0, None, 0)])
        response = api_client_factory().put(f'{PATH}?year={year}', data={'annual_salary_amount': 100.000})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['year'] == "2020"
        assert response.json()['total_tax_amount'] == "100.0000"

    def test_calculate_tax_for_special_year_if_there_are_no_policy_for_that_year(
        self,
        api_client_factory,
        taxes_policy_with_ranges_factory,
    ):
        year = 2020
        taxes_policy_with_ranges_factory(year=year-1, ranges_values=[(0, None, 100)])
        taxes_policy_with_ranges_factory(year=year+1, ranges_values=[(0, None, 0)])
        response = api_client_factory().put(f'{PATH}?year={year}', data={'annual_salary_amount': 100.000})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['year'] == "2020"
        assert response.json()['total_tax_amount'] == "100.0000"

    def test_try_to_calculate_tax_with_less_then_zero_salary(self, api_client_factory):
        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': -50.000})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_try_to_calculate_tax_with_too_long_salary_value(self, api_client_factory):
        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': "50."+("0"*9999999)})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client_factory().put(f'{PATH}?detailed=true', data={'annual_salary_amount': ("0"*99999999)+".1"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_try_to_calculate_tax_with_invalid_salary_value(self, api_client_factory, fake):
        valid_values = [10, 10.0, "10", "10.0"]
        invalid_values = [fake.word(), "", None, [1, 2, 3], {"some": "data"}, "10,0", "10.0.0"]
        for val in valid_values:
            assert api_client_factory().put(
                f'{PATH}?detailed=true',
                data={'annual_salary_amount': val}
            ).status_code == status.HTTP_200_OK
        for val in invalid_values:
            assert api_client_factory().put(
                f'{PATH}?detailed=true',
                data={'annual_salary_amount': val}
            ).status_code == status.HTTP_400_BAD_REQUEST

    def test_try_to_calculate_tax_with_invalid_year(self, api_client_factory, fake):
        response = api_client_factory().put(f'{PATH}?year={fake.word()}', data={'annual_salary_amount': 50.000})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client_factory().put(f'{PATH}?year=-20', data={'annual_salary_amount': 50.000})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = api_client_factory().put(f'{PATH}?year=20.20', data={'annual_salary_amount': 50.000})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_try_to_calculate_tax_with_invalid_detailed_param(self, api_client_factory, fake):
        response = api_client_factory().put(f'{PATH}?detailed={fake.word()}', data={'annual_salary_amount': 50.000})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
