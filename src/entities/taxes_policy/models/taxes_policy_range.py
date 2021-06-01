from typing import Optional, Iterable, TYPE_CHECKING
if TYPE_CHECKING:
    from .taxes_policy import TaxesPolicy

from common import models
from common.decimal import Decimal
from common.validators import MaxValueValidator


class TaxesPolicyRangeManager(models.Manager):
    pass


class TaxesPolicyRange(models.Model):

    amount_from: Decimal = models.DecimalField(default=0, decimal_places=4, max_digits=20)
    amount_to: Optional[Decimal] = models.DecimalField(null=True, decimal_places=4, max_digits=20)
    percent: int = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=100)], default=0)

    taxes_policies: Iterable['TaxesPolicy']

    objects: TaxesPolicyRangeManager = TaxesPolicyRangeManager()

    def __str__(self):
        return f'{self.percent}% between {self.amount_from} up to {self.amount_to or "the end"}.'

    class Meta:
        db_table = 'taxes_policy_range'
