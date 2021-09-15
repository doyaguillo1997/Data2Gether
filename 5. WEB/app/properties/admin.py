from django.contrib import admin

from app.properties.models import Property


class PropertyAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "cadastre", "external_id", "buyed_price")
    search_fields = ("id", "account__name", "external_id")


admin.site.register(Property, PropertyAdmin)
