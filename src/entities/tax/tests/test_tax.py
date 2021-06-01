import json
from collections import OrderedDict

import pytest

from common.datetime import get_current_year
from common.decimal import Decimal
from entities.tax.models import Tax
from entities.tax.models.tax import TaxRangeLine, TaxRangeLinesList
from entities.taxes_policy.models import TaxesPolicyRange
from entities.tax.serializers import TaxOutputSerializer


@pytest.mark.django_db
class TestTax:

    def test_init(self, fake):
        annual_salary_amount = fake.pydecimal(positive=True)
        tax = Tax(annual_salary_amount=annual_salary_amount)
        assert tax.annual_salary_amount == annual_salary_amount
        assert tax.year == get_current_year()

        year = fake.pyint(2000, 2030)
        tax = Tax(annual_salary_amount=annual_salary_amount, year=year)
        assert tax.year == year

    def test_annual_salary_amount_available_types(self, fake):
        salary = [
            fake.pydecimal(positive=True),
            '120.00',
            120.00,
            120
        ]
        for amount in salary:
            tax = Tax(amount)
            assert tax.annual_salary_amount == Decimal(amount)

    def test_year_available_types(self, fake):
        years = [2020, '2020', 2020.0]
        for year in years:
            tax = Tax(fake.pydecimal(positive=True), year=year)
            assert tax.year == year

    def test_range_line_calculation(self, taxes_policy_range_factory):
        for policy_range, salary, expected in [
            (taxes_policy_range_factory(amount_from=0, amount_to=50, percent=50), 100, 25),
            (taxes_policy_range_factory(amount_from=0, amount_to=50, percent=100), 100, 50),
            (taxes_policy_range_factory(amount_from=0, amount_to=50, percent=0), 100, 0),
            (taxes_policy_range_factory(amount_from=10, amount_to=50, percent=50), 100, 20),
            (taxes_policy_range_factory(amount_from=10, amount_to=50, percent=50), 40, 15),
            (taxes_policy_range_factory(amount_from=10, amount_to=50, percent=50), 5, 0),
        ]:
            assert TaxRangeLine(tax_policy_range=policy_range, annual_salary_amount=salary).amount == expected

    def test_get_total_amount_from_list(self, taxes_policy_range_factory):
        expected_sum = 0.0
        range_lines_list = TaxRangeLinesList()
        for policy_range, salary, expected in [
            (taxes_policy_range_factory(amount_from=0, amount_to=50, percent=50), 100, 25),
            (taxes_policy_range_factory(amount_from=0, amount_to=50, percent=100), 100, 50),
            (taxes_policy_range_factory(amount_from=0, amount_to=50, percent=0), 100, 0),
            (taxes_policy_range_factory(amount_from=10, amount_to=50, percent=50), 100, 20),
            (taxes_policy_range_factory(amount_from=10, amount_to=50, percent=50), 40, 15),
            (taxes_policy_range_factory(amount_from=10, amount_to=50, percent=50), 5, 0),
        ]:
            range_lines_list.append(TaxRangeLine(tax_policy_range=policy_range, annual_salary_amount=salary))
            expected_sum += expected

        assert range_lines_list.total_amount == expected_sum

    def test_get_total_amount(self, taxes_policy_factory):
        ranges = TaxesPolicyRange.objects.bulk_create([
            TaxesPolicyRange(amount_from=0, amount_to=12.500, percent=0),
            TaxesPolicyRange(amount_from=12.501, amount_to=50.000, percent=20),
            TaxesPolicyRange(amount_from=50.001, amount_to=150.000, percent=40),
            TaxesPolicyRange(amount_from=150.000, amount_to=None, percent=45),
        ])
        policy = taxes_policy_factory()
        policy.ranges.set(ranges)

        annual_salary_amount = 52.000
        tax = Tax(annual_salary_amount=annual_salary_amount, year=policy.year)
        assert round(tax.range_lines.total_amount, 2) == Decimal('8.30')
        assert tax.range_lines[0].amount == 0
        assert round(tax.range_lines[1].amount, 2) == Decimal('7.5')
        assert round(tax.range_lines[2].amount, 2) == Decimal('0.80')

    def test_output_serializer(self, taxes_policy_factory):
        ranges = TaxesPolicyRange.objects.bulk_create([
            TaxesPolicyRange(amount_from=0, amount_to=12.500, percent=0),
            TaxesPolicyRange(amount_from=12.501, amount_to=50.000, percent=20),
            TaxesPolicyRange(amount_from=50.001, amount_to=150.000, percent=40),
            TaxesPolicyRange(amount_from=150.000, amount_to=None, percent=45),
        ])
        policy = taxes_policy_factory(year=2000)
        policy.ranges.set(ranges)

        annual_salary_amount = 52.000
        tax = Tax(annual_salary_amount=annual_salary_amount, year=policy.year)
        serializer = TaxOutputSerializer(tax=tax)
        assert serializer.data == OrderedDict(
            annual_salary_amount="52.0000",
            year=str(policy.year),
            total_tax_amount="8.2994",
        )
        assert json.dumps(serializer.data)

        serializer = TaxOutputSerializer(tax=tax, detailed=True)
        assert serializer.data == OrderedDict([
            ('annual_salary_amount', '52.0000'),
            ('year', '2000'),
            ('total_tax_amount', '8.2994'),
            ('details', [
                OrderedDict([
                    ('amount_from', '0.0000'),
                    ('amount_to', '12.5000'),
                    ('percent', '0'),
                    ('tax_amount', '0.0000')
                ]),
                OrderedDict([
                    ('amount_from', '12.5010'),
                    ('amount_to', '50.0000'),
                    ('percent', '20'),
                    ('tax_amount', '7.4998')
                ]),
                OrderedDict([
                    ('amount_from', '50.0010'),
                    ('amount_to', '150.0000'),
                    ('percent', '40'),
                    ('tax_amount', '0.7996')
                ]),
                OrderedDict([
                    ('amount_from', '150.0000'),
                    ('amount_to', '*'),
                    ('percent', '45'),
                    ('tax_amount', '0.0000')
                ])
            ])
        ])
        assert json.dumps(serializer.data)
