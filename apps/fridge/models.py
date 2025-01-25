from django.db import models
from apps.common.models import BaseModel


class Refrigerator(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    year = models.CharField(max_length=4)

    class Meta:
        verbose_name = "Muzlatgich "
        verbose_name_plural = "Muzlatgichlar "

    def __str__(self):
        return self.name


class ElectricityBill(BaseModel):
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Elektr energiya to'lovi "
        verbose_name_plural = "Elektr energiyalar to'lovlari "

    def __str__(self):
        return self.refrigerator