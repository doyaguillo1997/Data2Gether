from django.contrib.gis.db import models


class Model(models.Model):
    model = models.BinaryField("Modelo")
    name = models.TextField("Name")
    version = models.FloatField("Version")
