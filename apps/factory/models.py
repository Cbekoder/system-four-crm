from django.db import models, transaction
from apps.common.models import BaseModel, BasePerson,CURRENCY_TYPE
from django.db.models import F

from apps.common.utils import convert_currency
from apps.main.models import Expense
from apps.users.models import User


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


class UserDailyWork(BaseModel):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Kunlik ish"
        verbose_name_plural = "Kunlik ishlar "
        ordering = ['-created_at']


    def delete(self, *args, **kwargs):
        with transaction.atomic():
            related_basket_counts = UserBasketCount.objects.filter(user_daily_work=self)

            for basket_count in related_basket_counts:
                basket_count.delete()

            super().delete(*args, **kwargs)


class UserBasketCount(models.Model):
    user_daily_work = models.ForeignKey(UserDailyWork, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True, blank=False, related_name='basket_count')
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Ishchi savat soni"
        verbose_name_plural = "Ishchi savat sonlari "

    def __str__(self):
        return self.user_daily_work.worker.full_name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = UserBasketCount.objects.get(pk=self.pk)

                prev.basket.quantity = F('quantity') - prev.quantity
                prev.basket.save(update_fields=['quantity'])
                prev.basket.refresh_from_db()

                prev.user_daily_work.amount = F('amount') - (prev.quantity * prev.basket.price)
                prev.user_daily_work.save(update_fields=['amount'])

                prev.user_daily_work.worker.balance = F('balance') - (prev.quantity * prev.basket.per_worker_fee)
                prev.user_daily_work.worker.save(update_fields=['balance'])

            super().save(*args, **kwargs)

            self.basket.quantity = F('quantity') + self.quantity
            self.basket.save(update_fields=['quantity'])

            self.user_daily_work.worker.balance = F('balance') + self.quantity * self.basket.per_worker_fee
            self.user_daily_work.worker.save(update_fields=['balance'])

            self.user_daily_work.amount = F('amount') + (self.quantity * self.basket.price)
            self.user_daily_work.save(update_fields=['amount'])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.basket.quantity = F('quantity') - self.quantity
            self.basket.save(update_fields=['quantity'])

            self.user_daily_work.worker.balance = F('balance') - self.quantity * self.basket.per_worker_fee
            self.user_daily_work.worker.save(update_fields=['balance'])

            self.user_daily_work.amount = F('amount') - (self.quantity * self.basket.price)
            self.user_daily_work.save(update_fields=['amount'])

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



class SalaryPayment(BaseModel):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="salary_payments_factory")


    def save(self, *args, **kwargs):

        if self.pk:
            prev=SalaryPayment.objects.get(pk=self.pk)
            if prev.currency_type != self.worker.currency_type:
                prev.amount = convert_currency(prev.currency_type, self.worker.currency_type, prev.amount)
            self.worker.balance+=prev.amount

        if self.worker.currency_type != self.currency_type:
            amount = convert_currency(self.currency_type, self.worker.currency_type, self.amount)
            self.worker.balance-=amount
            self.worker.save()
        else:
            self.worker.balance -= self.amount
            self.worker.save()

        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Oylik maosh "
        verbose_name_plural = "Oylik maosh "
        ordering = ['-created_at']


    def __str__(self):
        return self.worker.first_name

    def delete(self, *args, **kwargs):
        self.worker.balance+=self.amount
        self.worker.save(update_fields=['balance'])
        Expense.objects.filter(description__contains=f"| {self.id}").delete()
        super().delete(*args, **kwargs)


