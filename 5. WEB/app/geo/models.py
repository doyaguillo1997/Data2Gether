from django.contrib.gis.db import models


class GeoZone(models.Model):
    level = models.ForeignKey(
        "GeoLevel", null=True, blank=True, on_delete=models.SET_NULL
    )
    parent = models.ForeignKey(
        "GeoZone", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.TextField("Nombre")
    polygon = models.MultiPolygonField("Poligono")

    def __str__(self):
        return self.name

    @property
    def centroid(self):
        return self.polygon.centroid


class GeoLevel(models.Model):
    level = models.TextField("Nivel")

    def __str__(self):
        return self.level
