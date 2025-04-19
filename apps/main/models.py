from pyexpat.errors import messages

from django.core.cache import cache
from django.db import models, transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError
from apps.common.services.logging import Telegram
from apps.common.models import BaseModel, SECTION_CHOICES, BasePerson, CURRENCY_TYPE, SECTION_TO_KIRILL
from apps.common.utils import convert_currency
from apps.users.models import User


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
            if self.pk:
                prev = Expense.objects.get(id=self.pk)
                User.objects.filter(id=prev.user.id).update(
                    balance=F("balance") + convert_currency(prev.currency_type, prev.user.currency_type, prev.amount))

            super().save(*args, **kwargs)

            User.objects.filter(id=self.user.id).update(
                balance=F("balance") - convert_currency(self.currency_type, self.user.currency_type, self.amount)
            )

            if self.user.role == "CEO":
                self.status = 'verified'
                self.save(update_fields=['status'])

            message = f"💸 Харажат\n🔣 {SECTION_TO_KIRILL[self.section]}\n🆔 {self.id}\n🏷 {self.reason}\n📝 {self.description}\n👤 {self.user.get_full_name()}\n➖ {self.amount} {self.currency_type}"
            Telegram.send_log(message, app_button=True)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            User.objects.filter(id=self.user.id).update(
                balance=F('balance') + convert_currency(
                    self.currency_type, self.user.currency_type, self.amount
                )
            )
            super().delete(*args, **kwargs)

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
            if self.pk:
                prev = Income.objects.get(id=self.pk)
                User.objects.filter(id=prev.user.id).update(
                    balance=F("balance") - convert_currency(prev.currency_type, prev.user.currency_type, prev.amount))

            super().save(*args, **kwargs)

            User.objects.filter(id=self.user.id).update(
                balance=F("balance") + convert_currency(self.currency_type, self.user.currency_type, self.amount)
            )

            if self.user.role == "CEO":
                self.status = 'verified'
                self.save(update_fields=['status'])

            message = f"💸 Кирим\n🔣 {SECTION_TO_KIRILL[self.section]}\n🆔 {self.id}\n🏷 {self.reason}\n📝 {self.description}\n👤 {self.user.get_full_name()}\n➕ {self.amount} {self.currency_type}"
            Telegram.send_log(message, app_button=True)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            User.objects.filter(id=self.user.id).update(
                balance=F('balance') - convert_currency(
                    self.currency_type, self.user.currency_type, self.amount
                )
            )
            super().delete(*args, **kwargs)


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
            if self.pk:
                prev = MoneyCirculation.objects.get(id=self.pk)
                prev_converted_amount = prev.amount
                if prev.acquaintance.currency_type != prev.currency_type:
                    prev_converted_amount = convert_currency(prev.currency_type, prev.acquaintance.currency_type,
                                                             prev.amount)

                if prev.type == "get":
                    User.objects.filter(id=prev.creator.id).update(
                        balance=F('balance') - convert_currency(prev.currency_type, prev.creator.currency_type,
                                                                prev.amount)
                    )
                    if prev.acquaintance.landing > 0:
                        if prev.acquaintance.landing >= prev_converted_amount:
                            prev.acquaintance.landing += prev_converted_amount
                        else:
                            extra_debt_reversed = prev_converted_amount - prev.acquaintance.landing
                            prev.acquaintance.landing = 0
                            prev.acquaintance.debt -= extra_debt_reversed
                    else:
                        prev.acquaintance.debt -= prev_converted_amount

                elif prev.type == "give":
                    User.objects.filter(id=prev.creator.id).update(
                        balance=F('balance') + convert_currency(prev.currency_type, prev.creator.currency_type,
                                                                prev.amount)
                    )
                    if prev.acquaintance.debt > 0:
                        if prev.acquaintance.debt >= prev_converted_amount:
                            prev.acquaintance.debt += prev_converted_amount
                        else:
                            extra_landing_reversed = prev_converted_amount - prev.acquaintance.debt
                            prev.acquaintance.debt = 0
                            prev.acquaintance.landing -= extra_landing_reversed
                    else:
                        prev.acquaintance.landing -= prev_converted_amount
                prev.acquaintance.save()
            else:
                message = f"💸 Пул олди-берди\n🏷 {self.description}\n👤 {self.acquaintance.full_name}\n➕ {self.amount} {self.currency_type}"
                Telegram.send_log(message, app_button=True)

            converted_amount = self.amount
            if self.acquaintance.currency_type != self.currency_type:
                converted_amount = convert_currency(self.currency_type, self.acquaintance.currency_type, self.amount)
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
                User.objects.filter(id=self.creator.id).update(
                    balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount)
                )
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
                User.objects.filter(id=self.creator.id).update(
                    balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount)
                )
            self.acquaintance.landing = round(self.acquaintance.landing, 2)
            self.acquaintance.debt = round(self.acquaintance.debt, 2)
            self.acquaintance.save()

            if self.creator.role == "CEO":
                self.status = 'verified'

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            converted_amount = self.amount
            if self.acquaintance.currency_type != self.currency_type:
                converted_amount = convert_currency(self.currency_type, self.acquaintance.currency_type, self.amount)

            if self.type == "get":
                User.objects.filter(id=self.creator.id).update(
                    balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount)
                )
                if self.acquaintance.landing > 0:
                    if self.acquaintance.landing >= converted_amount:
                        self.acquaintance.landing += converted_amount
                    else:
                        extra_debt_reversed = converted_amount - self.acquaintance.landing
                        self.acquaintance.landing = 0
                        self.acquaintance.debt -= extra_debt_reversed
                else:
                    self.acquaintance.debt -= converted_amount

            elif self.type == "give":
                User.objects.filter(id=self.creator.id).update(
                    balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount)
                )
                if self.acquaintance.debt > 0:
                    if self.acquaintance.debt >= converted_amount:
                        self.acquaintance.debt += converted_amount
                    else:
                        extra_landing_reversed = converted_amount - self.acquaintance.debt
                        self.acquaintance.debt = 0
                        self.acquaintance.landing -= extra_landing_reversed
                else:
                    self.acquaintance.landing -= converted_amount

            self.acquaintance.landing = round(self.acquaintance.landing, 2)
            self.acquaintance.debt = round(self.acquaintance.debt, 2)
            self.acquaintance.save()

            message = f"🗑 Пул олди-берди ўчирилди\n🏷 {self.description}\n👤 {self.acquaintance.full_name}\n➖ {self.amount} {self.currency_type}"
            Telegram.send_log(message, app_button=True)

            super().delete(*args, **kwargs)

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


TRANSACTION_TYPE = (
    ('give', 'Berish'),
    ('get', 'Olish')
)

class TransactionToSection(BaseModel):
    section = models.CharField(max_length=30, choices=SECTION_CHOICES)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=CIRCULATION_TYPE_CHOICES)
    date = models.DateField(null=True, blank=True)
    status = None

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
                if prev.type == "get":
                    if prev.creator.role == 'admin':
                        User.objects.filter(id=prev.creator.id).update(
                            balance=F('balance') + convert_currency(prev.currency_type, prev.creator.currency_type, prev.amount))
                    else:
                        User.objects.filter(id=prev.creator.id).update(
                            balance=F('balance') + convert_currency(prev.currency_type, prev.creator.currency_type, prev.amount))
                else:
                    if prev.creator.role == 'admin':
                        User.objects.filter(id=prev.creator.id).update(
                            balance=F('balance') - convert_currency(prev.currency_type, prev.creator.currency_type, prev.amount))
                    else:
                        User.objects.filter(id=prev.creator.id).update(
                            balance=F('balance') - convert_currency(prev.currency_type, prev.creator.currency_type, prev.amount))

            super().save(*args, **kwargs)

            if self.type == "get":
                if self.creator.role == "admin":
                    User.objects.filter(id=self.creator.id).update(
                        balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount))
                else:
                    User.objects.filter(id=self.creator.id).update(
                        balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount))
            else:
                if self.creator.role == "admin":
                    User.objects.filter(id=self.creator.id).update(
                        balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount))
                else:
                    User.objects.filter(id=self.creator.id).update(
                        balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount))


class BankAccount(BaseModel):
    company = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    balance = models.FloatField(default=0)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    status = None

    def __str__(self):
        return f"{self.company} - {self.account_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


ACCOUNT_HISTORY_TYPE_CHOICES = (
    ('income', 'Kirim'),
    ('outcome', 'Chiqim')
)

REASON_CHOICES = (
    ('contact_income', 'Shartnoma puli'), # for income
    ('tax', 'Soliq'),                #
    ('tir', 'TIR uchun to\'lov'),    ## for outcome
    ('to_cash', 'Naqdlashtirish'),   #
    ('other', 'Boshqa'),             #
)

class AccountHistory(BaseModel):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(null=True, blank=True, max_length=100, choices=REASON_CHOICES)
    description = models.TextField(null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=ACCOUNT_HISTORY_TYPE_CHOICES)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    status = None

    class Meta:
        verbose_name = "Bank amaoliyoti"
        verbose_name_plural = "Bank amaliyotlari"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.account} - {self.transaction_type} - {self.amount}"
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = AccountHistory.objects.get(id=self.pk)
                if prev.transaction_type == "income":
                    BankAccount.objects.filter(id=prev.account.id).update(
                        balance=F('balance') - convert_currency(prev.currency_type, prev.account.currency_type, prev.amount))
                else:
                    BankAccount.objects.filter(id=prev.account.id).update(
                        balance=F('balance') + convert_currency(prev.currency_type, prev.account.currency_type, prev.amount))
            else:
                if self.transaction_type == "income":
                    t_type = "💰 Кирим"
                    arithmetic = "➕"
                elif self.transaction_type == "outcome":
                    t_type = "💸 Чиқим"
                    arithmetic = "➖"
                else:
                    raise ValidationError("Invalid transaction type")
                message = f"🏦 Банк амалиёти\n{t_type}\n💳{self.account.bank_name} | {self.account.account_number}\n🏷 {self.reason }\n📝 { self.description }\n{arithmetic} {self.amount} {self.currency_type}"
                Telegram.send_log(message, app_button=True)
            super().save(*args, **kwargs)

            if self.transaction_type == "income":
                BankAccount.objects.filter(id=self.account.id).update(
                    balance=F('balance') + convert_currency(self.currency_type, self.account.currency_type, self.amount))
            elif self.transaction_type == "outcome":
                BankAccount.objects.filter(id=self.account.id).update(
                    balance=F('balance') - convert_currency(self.currency_type, self.account.currency_type, self.amount))
            else:
                raise ValidationError("Invalid transaction type")

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            if self.transaction_type == "income":
                BankAccount.objects.filter(id=self.account.id).update(
                    balance=F('balance') - convert_currency(self.currency_type, self.account.currency_type, self.amount))
            elif self.transaction_type == "outcome":
                BankAccount.objects.filter(id=self.account.id).update(
                    balance=F('balance') + convert_currency(self.currency_type, self.account.currency_type, self.amount))
            super().delete(*args, **kwargs)


class DailyRemainder(BaseModel):
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = None
    creator = None

    class Meta:
        verbose_name = "Kunlik qoldiq "
        verbose_name_plural = "Kunlik qoldiqlar "
        ordering = ['-created_at']

    def __str__(self):
        return str(self.created_at)

