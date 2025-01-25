from django.db import models
from apps.common.models import BaseModel, BasePerson


class Worker(BasePerson):
    class Meta:
        verbose_name = "Ishchi"
        verbose_name_plural = "Ishchilar"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class Basket(BaseModel):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    weight = models.FloatField()
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    per_worker_fee = models.FloatField()

    class Meta:
        verbose_name = "Savat "
        verbose_name_plural = "Savatlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class DailyWork(BaseModel):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Kunlik ish"
        verbose_name_plural = "Kunlik ishlar "
        ordering = ['-created_at']


class RawMaterial(BaseModel):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Xomashyo "
        verbose_name_plural = "Xomashyolar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Supplier(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Ta'minotchi "
        verbose_name_plural = "Ta'minotchilar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class RawMaterialHistory(BaseModel):
    supplier = models.CharField(max_length=100)
    weight = models.FloatField(default=0)
    price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Xomashyo tarixi "
        verbose_name_plural = "Xomashyo tarixi "
        ordering = ['-created_at']

    def __str__(self):
        return self.supplier


class Client(BasePerson):
    class Meta:
        verbose_name = "Mijoz "
        verbose_name_plural = "Mijozlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

class Sale(BaseModel):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    class Meta:
        verbose_name = "Sotuv "
        verbose_name_plural = "Sotuvlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.basket





