from typing import Callable, Optional

import pytest

from common.decimal import Decimal
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange


@pytest.fixture
def taxes_policy_factory(fake) -> Callable:
    def create(year: Optional[int] = None) -> TaxesPolicy:
        year = year or fake.pyint(1900, 2021)
        return TaxesPolicy.objects.create(year=year)
    return create


@pytest.fixture
def taxes_policy_range_factory(fake) -> Callable:
    def create(
        amount_from: Optional[Decimal] = None, amount_to: Optional[Decimal] = None, percent: Optional[int] = None
    ) -> TaxesPolicyRange:
        amount_from = amount_from or fake.pyint(0, 5000)
        amount_to = amount_to or amount_from + fake.pyint(0, 5000)
        percent = percent or fake.pyint(0, 100)
        return TaxesPolicyRange.objects.create(amount_from=amount_from, amount_to=amount_to, percent=percent)
    return create