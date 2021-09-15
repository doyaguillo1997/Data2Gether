from django.contrib import admin

from app.external_sources.csv.models import Load
from app.external_sources.csv.models import PropertyDirty


class LoadAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "date", "name", "mapper")
    search_fields = ("account__name", "date", "name")


class PropertyDirtyAdmin(admin.ModelAdmin):
    list_display = ("load", "data")
    search_fields = ("load__account__name", "load__name", "load__date")


admin.site.register(Load, LoadAdmin)
admin.site.register(PropertyDirty, PropertyDirtyAdmin)
