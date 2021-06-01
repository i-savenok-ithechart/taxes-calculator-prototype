from typing import Optional

from common import models


class TaxesPolicyManager(models.Manager):
    pass


class TaxesPolicy(models.Model):

    year: Optional[int] = models.PositiveIntegerField(unique=True, null=False, blank=False)
    ranges = models.ManyToManyField('taxes_policy.TaxesPolicyRange', related_name='taxes_policies')

    objects: TaxesPolicyManager = TaxesPolicyManager()

    class Meta:
        db_table = 'taxes_policy'
        verbose_name = 'Taxes policies'

    def __str__(self):
        return str(self.year)


# class TaxesPolicyToTaxesRange(models.Model): todo
#     policy = models.ForeignKey('taxes_policy.TaxesPolicy', on_delete=models.CASCADE)
#     range = models.ForeignKey('taxes_policy.TaxesPolicyRange', on_delete=models.CASCADE)
#
#     def clean(self) -> None:
#         return super(TaxesPolicyToTaxesRange, self).clean()
