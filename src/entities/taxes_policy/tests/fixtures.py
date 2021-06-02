from typing import Callable, List, Optional, Tuple

import pytest

from common.decimal import Decimal
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange


@pytest.fixture
def taxes_policy_factory(fake) -> 'Callable':
    def create(year: Optional[int] = None) -> TaxesPolicy:
        year = year or fake.pyint(1900, 2021)
        return TaxesPolicy.objects.create(year=year)
    return create


@pytest.fixture
def taxes_policy_range_factory(fake) -> Callable:
    def create(
        amount_from: Optional[Decimal] = None, amount_to: Optional[Decimal] = None, percent: Optional[int] = None
    ) -> TaxesPolicyRange:
        if amount_from is None:
            amount_from = fake.pyint(0, 5000)
        if amount_to is None:
            amount_to = amount_from + fake.pyint(0, 5000)
        if percent is None:
            percent = fake.pyint(0, 100)
        return TaxesPolicyRange.objects.create(amount_from=amount_from, amount_to=amount_to, percent=percent)
    return create


@pytest.fixture
def taxes_policy_with_ranges_factory():
    def create(year: Optional[int], ranges_values: List[Tuple[Decimal, Decimal, int]]) -> TaxesPolicy:
        # ranges_values: a list of tuples with amount_from, amount_to, percent

        policy = TaxesPolicy.objects.create(year=year)
        ranges = TaxesPolicyRange.objects.bulk_create([
            TaxesPolicyRange(amount_from=values[0], amount_to=values[1], percent=values[2]) for values in ranges_values
        ])
        policy.ranges.set(ranges)
        return policy
    return create
