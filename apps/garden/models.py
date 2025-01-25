from django.db import models
from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE

class Gardener(BasePerson):
    class Meta:
        verbose_name = "Bog'bon "
        verbose_name_plural = "Bog'bonlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class SalaryPayment(BaseModel):
    gardener = models.ForeignKey(Gardener, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="UZS")

    def __str__(self):
        return self.gardener.full_name