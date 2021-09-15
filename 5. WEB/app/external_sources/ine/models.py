from django.contrib.gis.db import models


class DemographicElement(models.Model):
    geo_zone = models.ForeignKey("geo.GeoZone", on_delete=models.CASCADE)
    pob_total = models.IntegerField("Población")
    count_households = models.IntegerField("Numero viviendas")
    avg_size_home = models.FloatField("Tamaño medio del hogar")
    unemployment_rate = models.FloatField("Tasa de paro")
    prop_without_studies = models.FloatField("Proporción sin estudios")
    prop_without_university_studies = models.FloatField(
        "Proporción sin estudios universitarios"
    )
    prop_with_university_studies = models.FloatField(
        "Proporción con estudios universitarios"
    )
    density = models.FloatField("Densidad (Habit/Hab)")
    avg_age = models.FloatField("Edad Media")
    index_youth = models.FloatField("Indice de juventud")
    index_dependency = models.FloatField("Indice de dependencia")
    index_active_population = models.FloatField("Indice de población activa")
    index_replacement_active_population = models.FloatField(
        "Indice de remplazo de población activa"
    )
    prop_born_outside = models.FloatField("Proporción nacidos fuera de España")
