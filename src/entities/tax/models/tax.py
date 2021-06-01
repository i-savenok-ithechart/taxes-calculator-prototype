from typing import Iterator

from common.datetime import get_current_year
from common.decimal import Decimal
from common.utils import InfinityLimit
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange


class Tax:
    annual_salary_amount: Decimal
    year: int
    _range_lines: 'TaxRangeLinesList[TaxRangeLine]' = None

    def __init__(self, annual_salary_amount: Decimal, year: int = None):
        self.annual_salary_amount = Decimal(annual_salary_amount)
        self.year = year or get_current_year()

    @property
    def range_lines(self):
        if self._range_lines is None:  # lazy
            taxes_policy = TaxesPolicy.objects.get_for_year(self.year)
            self._range_lines = TaxRangeLinesList(
                TaxRangeLine(tax_policy_range=policy_range, annual_salary_amount=self.annual_salary_amount)
                for policy_range in taxes_policy.ranges.all()
            )
        return self._range_lines


class TaxRangeLine:
    policy_range: TaxesPolicyRange
    amount: Decimal

    def __init__(self, tax_policy_range: TaxesPolicyRange, annual_salary_amount: Decimal):
        self.policy_range = tax_policy_range
        self._recalculate_amount(annual_salary_amount)

    def _recalculate_amount(self, annual_salary_amount: Decimal):
        calculated_amount = Decimal(0)
        if annual_salary_amount > self.policy_range.amount_from:

            if annual_salary_amount <= self.policy_range.amount_to:
                amount_before_range_ends = annual_salary_amount
            else:
                if isinstance(self.policy_range.amount_to, InfinityLimit):
                    amount_before_range_ends = annual_salary_amount
                else:
                    amount_before_range_ends = self.policy_range.amount_to

            amount_in_range = amount_before_range_ends - self.policy_range.amount_from
            calculated_amount = amount_in_range / 100 * self.policy_range.percent

        self.amount = calculated_amount


class TaxRangeLinesList(list):
    def __iter__(self) -> Iterator['TaxRangeLine']: return super(TaxRangeLinesList, self).__iter__()  # for type hints

    @property
    def total_amount(self):
        result = Decimal(0)
        for range_line in self:
            result += Decimal(range_line.amount)
        return result
