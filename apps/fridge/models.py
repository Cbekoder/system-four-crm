from django.db import models, transaction
from apps.common.models import BaseModel
from apps.common.utils import convert_currency


class Refrigerator(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    year = models.CharField(max_length=4)
    status = None
    creator = None

    class Meta:
        verbose_name = "Muzlatgich "
        verbose_name_plural = "Muzlatgichlar "

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
