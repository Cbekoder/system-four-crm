from django.db import models
from apps.common.models import BaseModel, BasePerson,CURRENCY_TYPE
from django.db.models import F
from apps.main.models import Expense

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
    creator = None

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
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Kunlik ish"
        verbose_name_plural = "Kunlik ishlar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.pk:
            prev = DailyWork.objects.get(pk=self.pk)

            self.basket.quantity = F('quantity') - prev.quantity
            self.basket.save(update_fields=['quantity'])
            self.basket.refresh_from_db()

            self.worker.balance = F('balance') - (prev.quantity * self.basket.per_worker_fee)
            self.worker.save(update_fields=['balance'])
            self.worker.balance = self.worker.balance + self.price

        self.price = self.quantity * self.basket.per_worker_fee
        super().save(*args, **kwargs)

        self.basket.quantity = F('quantity') + self.quantity
        self.basket.save(update_fields=['quantity'])
        self.basket.refresh_from_db()

        self.worker.balance = F('balance') + self.price
        self.worker.save(update_fields=['balance'])
        self.worker.refresh_from_db()

    def delete(self, *args, **kwargs):
        self.basket.quantity = F('quantity') - self.quantity
        self.basket.save(update_fields=['quantity'])

        self.worker.balance = F('balance') - self.price
        self.worker.save(update_fields=['balance'])
        super().delete(*args, **kwargs)


class RawMaterial(BaseModel):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    price = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Xomashyo "
        verbose_name_plural = "Xomashyolar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    creator = None

    class Meta:
        verbose_name = "Ta'minotchi "
        verbose_name_plural = "Ta'minotchilar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class RawMaterialHistory(BaseModel):
    supplier = models.CharField(max_length=100)
    weight = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")

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
    amount = models.FloatField(default=0)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    is_debt=models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sotuv "
        verbose_name_plural = "Sotuvlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.basket.name

    def save(self, *args, **kwargs):
        if self.pk:
            prev=Sale.objects.get(pk=self.pk)
            self.basket.quantity = F('quantity') + prev.quantity
            self.basket.save(update_fields=['quantity'])
        self.amount= self.quantity * self.basket.price
        self.basket.quantity = F('quantity') - self.quantity
        self.basket.save(update_fields=['quantity'])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.basket.quantity = F('quantity') + self.quantity
        self.basket.save(update_fields=['quantity'])
        super().delete(*args, **kwargs)







