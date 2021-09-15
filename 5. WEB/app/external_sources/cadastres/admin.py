from django.contrib import admin

from app.external_sources.cadastres.models import Cadastre
from app.external_sources.cadastres.models import ClassType
from app.external_sources.cadastres.models import Distribution
from app.external_sources.cadastres.models import PrimaryUse
from app.external_sources.cadastres.models import Subplot


class CadastreAdmin(admin.ModelAdmin):
    list_display = (
        "cadastral_reference",
        "type",
        "primary_use",
        "province",
        "municipality",
        "postal_code",
        "address",
        "builded_surface",
        "year_built",
        "participation_coefficient",
    )
    search_fields = (
        "cadastral_reference",
        "primary_use__text",
        "type__type",
        "province",
        "municipality",
        "postal_code",
        "address",
        "builded_surface",
        "year_built",
        "participation_coefficient",
    )


class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ("type",)
    search_fields = ("type",)


class PrimaryUseAdmin(admin.ModelAdmin):
    list_display = ("text",)
    search_fields = ("text",)


class DistributionAdmin(admin.ModelAdmin):
    list_display = (
        "cadastre",
        "princpial_use",
        "surface",
    )
    search_fields = (
        "cadastre__cadastral_reference",
        "princpial_use",
        "surface",
        "cadastre",
    )


class SubplotAdmin(admin.ModelAdmin):
    list_display = (
        "cadastre",
        "subplot_code",
        "cadastral_qualification",
        "cultivation_class",
        "surface",
        "productive_intensity",
    )
    search_fields = (
        "cadastre__cadastral_reference",
        "cadastral_qualification",
        "cultivation_class",
        "surface",
        "productive_intensity",
    )


admin.site.register(Cadastre, CadastreAdmin)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(PrimaryUse, PrimaryUseAdmin)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Subplot, SubplotAdmin)
