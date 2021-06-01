from typing import Optional, Iterable, TYPE_CHECKING, Tuple, Collection

from common.exceptions import ValidationError

if TYPE_CHECKING:
    from .taxes_policy import TaxesPolicy

from common import models
from common.decimal import Decimal
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
    pass


class TaxesPolicyRange(models.Model):

    amount_from: Decimal = models.DecimalField(default=0, decimal_places=4, max_digits=20)
    amount_to: Optional[Decimal] = models.DecimalField(decimal_places=4, max_digits=20)
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
