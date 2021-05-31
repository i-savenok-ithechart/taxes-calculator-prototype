from common import admin
from entities.taxes_policy.models import TaxesPolicy, TaxesPolicyRange


class TaxesPolicyAdmin(admin.ModelAdmin):
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
