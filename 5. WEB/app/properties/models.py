from django.contrib.gis.db import models


class Property(models.Model):
    account = models.ForeignKey(
        "accounts.Account",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    cadastre = models.ForeignKey(
        "cadastres.Cadastre",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    external_id = models.TextField()
    buyed_price = models.FloatField("Precio de compra")
    estimated_price = models.FloatField("Precio estimado", null=True, blank=True)

    class Meta:
        unique_together = (("account", "external_id"),)
        verbose_name_plural = "Properties"

    def __str__(self):
        return str(self.account) + " - " + self.external_id
