from django.contrib.gis.db import models


class Historic(models.Model):
    geo_zone = models.ForeignKey("geo.GeoZone", on_delete=models.CASCADE)
    date = models.DateField("Fecha")
    price = models.FloatField("Precio", null=True, blank=True)
    monthly_variation = models.FloatField("Variación mensual", null=True, blank=True)
    quarterly_variation = models.FloatField(
        "Variación trimestral", null=True, blank=True
    )
    annual_variation = models.FloatField("Variación anual", null=True, blank=True)
    conf_low = models.FloatField("Cota superior", null=True, blank=True)
    conf_up = models.FloatField("Cota inferior", null=True, blank=True)
    value_type = models.TextField("Tipo de valor", default="current")
