from typing import Optional, Any

from common import models
from entities.taxes_policy.models.taxes_policy_range import TaxesPolicyRange


class TaxesPolicyManager(models.Manager):

    def create(self, *args: Any, year: int = 0, **kwargs: Any) -> 'TaxesPolicy':
        return super(TaxesPolicyManager, self).create(*args, year=year, **kwargs)

    def create_defaults(self) -> 'TaxesPolicy':
        default_policy = self.create(year=0)
        default_policy_ranges = TaxesPolicyRange.objects.bulk_create([
            TaxesPolicyRange(amount_to=12.500),
            TaxesPolicyRange(amount_from=12.501, amount_to=50.000, percent=20),
            TaxesPolicyRange(amount_from=50.001, amount_to=150.000, percent=40),
            TaxesPolicyRange(amount_from=150.001, amount_to=None, percent=45),
        ])
        default_policy.ranges.set(default_policy_ranges)
        return default_policy

    def get_for_year(self, year: int) -> 'TaxesPolicy':
        """
        # todo describe that stuff
        """

        instance = self.prefetch_related('ranges').filter(year__lte=year).order_by('+year').first()
        if not instance:
            instance = self.create_defaults()

        return instance


class TaxesPolicy(models.Model):

    year: Optional[int] = models.PositiveIntegerField(unique=True, null=False, blank=False)
    ranges = models.ManyToManyField('taxes_policy.TaxesPolicyRange', related_name='taxes_policies')

    objects: TaxesPolicyManager = TaxesPolicyManager()

    class Meta:
        db_table = 'taxes_policy'
        verbose_name_plural = 'Taxes policies'

    def __str__(self):
        return str(self.year)
