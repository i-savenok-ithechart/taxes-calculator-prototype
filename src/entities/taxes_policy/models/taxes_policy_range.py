from typing import Optional, TYPE_CHECKING, Tuple, Any, Union

from common.exceptions import ValidationError

from common import models
from common.decimal import Decimal
from common.utils import InfinityLimit
from common.validators import MaxValueValidator


class TaxesPolicyRangeQuerySet(models.QuerySet):

    def find_first_overlapping_pair(self) -> Optional[Tuple['TaxesPolicyRange', 'TaxesPolicyRange']]:
        for policy_range in self:
            if TYPE_CHECKING:
                policy_range: 'TaxesPolicyRange'

            for other_policy_range in self:
                if policy_range is other_policy_range:
                    continue

                if policy_range.is_overlapping_with(other_policy_range):
                    return policy_range, other_policy_range


class TaxesPolicyRangeManager(models.Manager):

    def create(
        self,
        *args: Any,
        amount_from: Union[Decimal, int, str] = 0,
        amount_to: Union[Decimal, int, str],
        percent: int = 0,
        **kwargs: Any,
    ) -> 'TaxesPolicyRange':
        return super(TaxesPolicyRangeManager, self).create(
            *args,
            amount_from=amount_from,
            amount_to=amount_to,
            percent=percent,
            **kwargs,
        )


class TaxesPolicyRange(models.Model):

    amount_from: Decimal = models.DecimalField(default=0, decimal_places=4, max_digits=20)

    _amount_to: Optional[Decimal] = models.DecimalField(decimal_places=4, max_digits=20, null=True)
    """
        If amount_to value is null - it means that range includes all from "amount_from" to infinity.
    """
    @property
    def amount_to(self) -> Union[Decimal, InfinityLimit]: return self._amount_to or InfinityLimit()

    @amount_to.setter
    def amount_to(self, value: Union[Decimal, None, InfinityLimit]):
        self._amount_to = (value if not isinstance(value, InfinityLimit) else None)

    percent: int = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)

    taxes_policies: models.Manager

    objects: TaxesPolicyRangeManager = TaxesPolicyRangeManager.from_queryset(TaxesPolicyRangeQuerySet)()

    def __str__(self):
        return f'{self.percent}% between {self.amount_from} up to {self.amount_to or "the end"}.'

    def clean(self, *args, **kwargs) -> None:
        if not self._amount_to_is_greater_than_amount_from():
            raise ValidationError('End amount must be greater than start amount')
        return super(TaxesPolicyRange, self).clean()

    def _amount_to_is_greater_than_amount_from(self) -> bool: return self.amount_to > self.amount_from

    def is_overlapping_with(self, taxes_policy_range: 'TaxesPolicyRange') -> bool:
        return self.amount_from <= taxes_policy_range.amount_to and self.amount_to >= taxes_policy_range.amount_from

    class Meta:
        db_table = 'taxes_policy_range'
