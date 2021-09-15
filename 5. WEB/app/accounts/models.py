from django.contrib.gis.db import models


class Account(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Mapper(models.Model):
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    external_column = models.TextField()
    internal_column = models.TextField()
    field_type = models.CharField(max_length=50)
