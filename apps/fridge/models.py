from django.db import models
from apps.common.models import BaseModel
from apps.common.utils import convert_currency
from apps.main.models import Expense,Section


class Refrigerator(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    year = models.CharField(max_length=4)

    class Meta:
        verbose_name = "Muzlatgich "
        verbose_name_plural = "Muzlatgichlar "

    def __str__(self):
        return self.name


class ElectricityBill(Expense):
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Elektr energiya to'lovi "
        verbose_name_plural = "Elektr energiyalar to'lovlari "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reason:
            self.reason = "Muzlatich uchun elektr energiya to'lovi"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.refrigerator.name

class FridgeExpense(Expense):
    refrigerator = models.ForeignKey(Refrigerator, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.refrigerator.name

    def save(self, *args, **kwargs):
        if not self.section:
            garden_section = Section.objects.get_or_create(name="Muzlatgish")
            self.section = garden_section
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Xarajat "
        verbose_name_plural = "Xarajatlar "
        ordering = ['-created_at']