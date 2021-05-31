from django.contrib import admin as _admin
from django.contrib.admin import site as _site

admin = _admin
site = _site


class ModelAdmin(_admin.ModelAdmin):
    pass
