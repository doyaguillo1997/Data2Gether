from django.contrib.gis.db import models
from django.db.models import Sum


class Cadastre(models.Model):
    primary_use = models.ForeignKey(
        "PrimaryUse", null=True, blank=True, on_delete=models.SET_NULL
    )
    type = models.ForeignKey(
        "ClassType", null=True, blank=True, on_delete=models.SET_NULL
    )
    cadastral_reference = models.TextField("RC")
    address = models.TextField("Dirección")
    province = models.TextField("Provincia")
    municipality = models.TextField("Municipio")
    builded_surface = models.IntegerField("Metros cuadrados construidos")
    participation_coefficient = models.FloatField(
        "Coeficiente de participación en la parcela", default=100
    )
    year_built = models.IntegerField("Año de construcción", default=-1)
    location = models.PointField("Localización", null=True, blank=True)
    postal_code = models.CharField("CP", null=True, blank=True, max_length=32)

    def __str__(self):
        return self.cadastral_reference

    @property
    def floor(self):
        start = self.address.find("Pl:")
        return self.address[start + 3 : start + 5]

    @property
    def private_builded_surface(self):
        distributions = Distribution.objects.filter(
            cadastre=self.pk, princpial_use="VIVIENDA"
        )

        if distributions.count() > 0:
            return distributions.aggregate(Sum("surface"))["surface__sum"]

        print("Problemas con:", self.cadastral_reference)
        return self.builded_surface

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x


class ClassType(models.Model):
    type = models.TextField("Tipo de propiedad")

    def __str__(self):
        return self.type


class PrimaryUse(models.Model):
    text = models.TextField("Uso principal")

    def __str__(self):
        return self.text


class Distribution(models.Model):
    cadastre = models.ForeignKey("Cadastre", on_delete=models.CASCADE)
    princpial_use = models.TextField("Uso")
    surface = models.IntegerField("Superficie en metros cuadrados")

    def __str__(self):
        return self.princpial_use + str(self.surface)


class Subplot(models.Model):
    cadastre = models.ForeignKey("Cadastre", on_delete=models.CASCADE)
    subplot_code = models.TextField("Código")
    cadastral_qualification = models.TextField("Calificación")
    cultivation_class = models.TextField("Tipo de cultivo")
    surface = models.IntegerField("Superficie en metros cuadrados")
    productive_intensity = models.TextField("Intensidad productiva")

    def __str__(self):
        return self.subplot_code


class Road(models.Model):
    name = models.TextField("Nombre de la via")
    type = models.TextField("Tipo via", default="-1")
