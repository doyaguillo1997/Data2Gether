from django.contrib.gis.db import models


class School(models.Model):
    type = models.ForeignKey(
        "SchoolType", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.TextField("Nombre")
    address = models.TextField("Dirección")
    price = models.TextField("Precio")
    review = models.TextField("Valoración")
    description = models.TextField("Descripción")
    query = models.TextField("Petición")
    coord = models.PointField("Localización")
    price_level = models.SmallIntegerField("Nivel Precio")
    price_level_weights = models.FloatField("Peso Precio")

    def __str__(self):
        return self.name

    @property
    def latitude(self):
        return self.coord.y

    @property
    def longitude(self):
        return self.coord.x


class SchoolType(models.Model):
    type = models.TextField("Tipo")
