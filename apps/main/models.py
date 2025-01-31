from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from apps.common.models import BaseModel, SECTION_CHOICES, BasePerson, CURRENCY_TYPE
from apps.common.utils import convert_currency
from apps.users.models import User


class Expense(BaseModel):
    reason = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.reason


class Income(BaseModel):
    reason = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = "Kirim "
        verbose_name_plural = "Kirimlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.reason


class Acquaintance(BasePerson):
    """Qarz berishi va qarz olishi mumkin bo'lgan tanish bilishlari"""
    balance = None
    birth_date = None

    class Meta:
        verbose_name = "Tanish-bilish "
        verbose_name_plural = "Tanish-bilishlar"

    def __str__(self):
        return self.full_name


TYPE_CHOICES = (
    ('give', 'Berish'),
    ('get', 'Olish')
)

class MoneyCirculation(BaseModel):
    acquaintance = models.ForeignKey(Acquaintance, on_delete=models.SET_NULL, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Pul oldi-berdi "
        verbose_name_plural = "Pul oldi-berdilari "
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.acquaintance:
            raise ValidationError("Acquaintance is required")
        with transaction.atomic():
            converted_amount = self.amount
            if self.acquaintance.currency_type == self.currency_type:
                valid_currencies = ("USD", "UZS")
                if self.acquaintance.currency_type in valid_currencies and self.currency_type in valid_currencies:
                    converted_amount = convert_currency(self.currency_type, self.acquaintance.currency_type, self.amount)
                else:
                    raise ValidationError("Invalid currency type")
            if self.type == 'get':
                if self.acquaintance.landing > 0:
                    if self.acquaintance.landing >= converted_amount:
                        self.acquaintance.landing -= converted_amount
                    else:
                        extra_debt = converted_amount - self.acquaintance.landing
                        self.acquaintance.landing = 0
                        self.acquaintance.debt += extra_debt
                else:
                    self.acquaintance.debt += converted_amount
            elif self.type == 'give':
                if self.acquaintance.debt > 0:
                    if self.acquaintance.debt >= converted_amount:
                        self.acquaintance.debt -= converted_amount
                    else:
                        extra_landing = converted_amount - self.acquaintance.debt
                        self.acquaintance.debt = 0
                        self.acquaintance.landing += extra_landing
                else:
                    self.acquaintance.landing += converted_amount
            self.acquaintance.landing = round(self.acquaintance.landing, 2)
            self.acquaintance.debt = round(self.acquaintance.debt, 2)
            self.acquaintance.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return self.acquaintance.full_name if self.acquaintance else str(self.id)
