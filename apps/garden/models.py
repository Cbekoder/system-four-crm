from django.db import models
from rest_framework.exceptions import ValidationError

from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE
from apps.common.utils import convert_currency
from apps.users.models import User


class Gardener(BasePerson):
    class Meta:
        verbose_name = "Bog'bon "
        verbose_name_plural = "Bog'bonlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.creator.role == "CEO":
            self.status = 'verified'
        super().save(*args, **kwargs)


class SalaryPayment(BaseModel):
    gardener = models.ForeignKey(Gardener, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="UZS")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="garden_salary_payment_creator")

    class Meta:
        verbose_name = "Oylik maosh"
        verbose_name_plural = "Oylik maoshlar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):

        if self.pk:
            old_payment = SalaryPayment.objects.get(id=self.pk)
            old_amount = old_payment.amount
            if self.currency_type != old_payment.currency_type:
                valid_currencies = ("USD", "UZS")
                if old_payment.currency_type in valid_currencies and self.currency_type in valid_currencies:
                    old_amount = convert_currency(old_payment.currency_type, self.currency_type, old_amount)
            if self.amount != old_payment.amount:
                self.gardener.balance -= old_amount
            if self.gardener != old_payment.gardener:
                raise ValidationError("It is not allowed to change gardener")

        converted_amount = self.amount
        if self.gardener.currency_type == self.currency_type:
            valid_currencies = ("USD", "UZS")
            if self.gardener.currency_type in valid_currencies and self.currency_type in valid_currencies:
                converted_amount = convert_currency(self.currency_type, self.gardener.currency_type,
                                                    self.amount)
            else:
                raise ValidationError("Invalid currency type")

        self.gardener.balance += converted_amount
        self.gardener.save()

        if self.creator.role == "CEO":
            self.status = 'verified'

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.gardener.balance -= self.amount
        self.gardener.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.gardener.full_name



