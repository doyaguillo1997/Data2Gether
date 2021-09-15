from django.contrib.gis.db import models


class Load(models.Model):
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    mapper = models.JSONField()

    def __str__(self):
        return f"Client {self.account}: {self.name} ({self.date})"


class PropertyDirty(models.Model):
    load = models.ForeignKey(Load, on_delete=models.CASCADE)
    property = models.ForeignKey(
        "properties.Property", null=True, blank=True, on_delete=models.SET_NULL
    )
    data = models.JSONField()

    class Meta:
        verbose_name_plural = "Dirty Properties"
