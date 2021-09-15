from django.contrib import admin

from app.accounts.models import Account, Mapper


class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class MapperAdmin(admin.ModelAdmin):
    list_display = ("account", "external_column", "internal_column", "field_type")
    search_fields = ("account__name",)


admin.site.register(Account, AccountAdmin)
admin.site.register(Mapper, MapperAdmin)
