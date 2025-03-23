from django.core.cache import cache
from django.db import models, transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError
from apps.common.services.logging import Telegram
from apps.common.models import BaseModel, SECTION_CHOICES, BasePerson, CURRENCY_TYPE
from apps.common.utils import convert_currency
from apps.users.models import User

class CurrencyRate(BaseModel):
    usd = models.FloatField()
    rub = models.FloatField()

    def __str__(self):
        return str(self.created_at)

    class Meta:
        verbose_name = "Valyutalar kursi "
        verbose_name_plural = "Valyutalar kurslari "


    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            cache.set("UZS_rate", self.usd)
            cache.set("RUB_rate", round(self.usd / self.rub, 2))
            print(cache.get("RUB_rate"))


class Expense(BaseModel):
    reason = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses_created")
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        with transaction.atomic():

            super().save(*args, **kwargs)

            if self.user.role == "CEO":
                self.status = 'verified'
                self.save(update_fields=['status'])

            message = f"💸 Xarajat\n🔣 {self.section.title()}\n🆔 {self.id}\n🏷 {self.reason}\n📝 {self.description}\n👤 {self.user.get_full_name()}\n➖ {self.amount} {self.currency_type}"
            Telegram.send_log(message, app_button=True)

    def __str__(self):
        return self.reason


class Income(BaseModel):
    reason = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    section = models.CharField(max_length=30, choices=SECTION_CHOICES, null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Kirim "
        verbose_name_plural = "Kirimlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.reason

    def save(self, *args, **kwargs):
        with transaction.atomic():

            super().save(*args, **kwargs)

            if self.user.role == "CEO":
                self.status = 'verified'
                self.save(update_fields=['status'])

            message = f"💸 Kirim\n🔣 {self.section.title()}\n🆔 {self.id}\n🏷 {self.reason}\n📝 {self.description}\n👤 {self.user.get_full_name()}\n➖ {self.amount} {self.currency_type}"
            Telegram.send_log(message, app_button=True)


class Acquaintance(BasePerson):
    """Qarz berishi va qarz olishi mumkin bo'lgan tanish bilishlari"""
    balance = None
    birth_date = None

    class Meta:
        verbose_name = "Tanish-bilish "
        verbose_name_plural = "Tanish-bilishlar"

    def __str__(self):
        return self.full_name


CIRCULATION_TYPE_CHOICES = (
    ('give', 'Berish'),
    ('get', 'Olish')
)

class MoneyCirculation(BaseModel):
    acquaintance = models.ForeignKey(Acquaintance, on_delete=models.SET_NULL, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    type = models.CharField(max_length=20, choices=CIRCULATION_TYPE_CHOICES)

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

            if self.creator.role == "CEO":
                self.status = 'verified'

            super().save(*args, **kwargs)

    def __str__(self):
        return self.acquaintance.full_name if self.acquaintance else str(self.id)


class TransactionToAdmin(BaseModel):
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    status = None
    creator = None

    def __str__(self):
        return self.admin.get_full_name() if self.admin else str(self.id)

    class Meta:
        verbose_name = "Admin hisobiga pul o'tkazish"
        verbose_name_plural = "Admin hisobiga pul o'tkazishlar"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = TransactionToAdmin.objects.get(id=self.pk)
                converted_amount = convert_currency(prev.currency_type, "UZS", prev.amount)
                User.objects.filter(id=prev.creator.id).update(balance=F('balance') + converted_amount)

            super().save(*args, **kwargs)

            converted_amount = convert_currency(self.currency_type, "UZS", self.amount)
            User.objects.filter(id=self.creator.id).update(balance=F('balance') - converted_amount)


class TransactionToSection(BaseModel):
    section = models.CharField(max_length=30, choices=SECTION_CHOICES)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    status = None
    creator = None

    def __str__(self):
        return self.section

    class Meta:
        verbose_name = "Bo'lim hisobiga pul o'tkazish"
        verbose_name_plural = "Bo'lim hisobiga pul o'tkazishlar"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = TransactionToSection.objects.get(id=self.pk)
                converted_amount = convert_currency(prev.currency_type, "UZS", prev.amount)
                User.objects.filter(id=prev.creator.id).update(balance=F('balance') + converted_amount)

            super().save(*args, **kwargs)

            converted_amount = convert_currency(self.currency_type, "UZS", self.amount)
            User.objects.filter(id=self.creator.id).update(balance=F('balance') - converted_amount)



REMAINDER_TYPE_CHOICES = (
    ('auto', 'Avtomatik'),
    ('manual', 'Qo\'lda')
)

class DailyRemainder(BaseModel):
    amount = models.FloatField()
    type = models.CharField(max_length=20, choices=REMAINDER_TYPE_CHOICES, default="manual")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = None
    creator = None

    class Meta:
        verbose_name = "Kunlik qoldiq "
        verbose_name_plural = "Kunlik qoldiqlar "
        ordering = ['-created_at']

    def __str__(self):
        return str(self.created_at)

