from dataclasses import dataclass, field
from typing import Iterator

from common.datetime import get_current_year
from common.decimal import Decimal
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange


@dataclass
class Tax:
    annual_salary_amount: Decimal
    year: int = field(default_factory=get_current_year)

    _range_lines: 'TaxRangeLinesList[TaxRangeLine]' = None

    @property
    def range_lines(self):
        if not self._range_lines:  # lazy
            taxes_policy = ...
            self._range_lines = ...
        return self._range_lines


class TaxRangeLine:
    policy_range: TaxesPolicyRange
    amount: Decimal

    def __init__(self, tax_policy_range: TaxesPolicyRange, annual_salary_amount: Decimal):
        self.policy_range = tax_policy_range
        self._recalculate_amount(annual_salary_amount)

    def _recalculate_amount(self, annual_salary_amount):
        self.amount = ...


class TaxRangeLinesList(list):
    def __iter__(self) -> Iterator['TaxRangeLine']: return super(TaxRangeLinesList, self).__iter__()  # for type hints

    @property
    def total_amount(self): return ...
