from django.contrib.gis.db import models


class GoogleElement(models.Model):
    find_type = models.ForeignKey(
        "GoogleType", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.TextField("Nombre")
    rating = models.FloatField("Valoración")
    user_ratings_total = models.IntegerField("Número valoraciones")
    coord = models.PointField("Localización")
    price_level_missing = models.BooleanField("Falta Precio", default=False)
    price_level = models.IntegerField("Nivel Precio")
    price_level_weights = models.FloatField("Peso Precio")

    def __str__(self):
        return self.name

    @property
    def latitude(self):
        return self.coord.y

    @property
    def longitude(self):
        return self.coord.x


class GoogleType(models.Model):
    type = models.TextField("Tipo")
