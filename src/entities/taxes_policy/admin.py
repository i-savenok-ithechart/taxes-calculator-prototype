from typing import Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from entities.taxes_policy.models.taxes_policy_range import TaxesPolicyRangeQuerySet

from common import admin
from common.forms import ModelForm
from common.exceptions import ValidationError
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange


class TaxesPolicyAdminForm(ModelForm):
    class Meta:
        model = TaxesPolicy
        fields = ['year', 'ranges']

    def clean(self) -> Dict[str, Any]:
        self._validate_ranges_for_overlapping()
        return super(TaxesPolicyAdminForm, self).clean()

    def _validate_ranges_for_overlapping(self):
        if isinstance(self.cleaned_data, dict):
            ranges_qs: 'TaxesPolicyRangeQuerySet' = self.cleaned_data.get('ranges')
            overlapping_pair = ranges_qs.find_first_overlapping_pair()
            if overlapping_pair:
                raise ValidationError(f'The range {overlapping_pair[0]} is overlapping with {overlapping_pair[1]}')


class TaxesPolicyAdmin(admin.ModelAdmin):
    form = TaxesPolicyAdminForm
    search_fields = (
        'year',
    )
    list_display = (
        'year',
        'created_at',
        'updated_at',
    )


class TaxesPolicyRangeAdmin(admin.ModelAdmin):
    list_display = (
        'amount_from',
        'amount_to',
        'percent',
    )


admin.site.register(TaxesPolicy, TaxesPolicyAdmin)
admin.site.register(TaxesPolicyRange, TaxesPolicyRangeAdmin)
