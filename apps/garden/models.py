from django.db import models, transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE
from apps.common.services.logging import Telegram
from apps.common.utils import convert_currency
from apps.users.models import User


# Garden Models
class Garden(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name='garden_creator', on_delete=models.CASCADE)
    status = None

    class Meta:
        verbose_name = "Bog' "
        verbose_name_plural = "Bog'lar "

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            message = f"🏡 Янги боғ қўшилди 🆕\n🏷 {self.name} \n📝 {self.description}\n👤 {self.creator.get_full_name()}"
            Telegram.send_log(message, app_button=True)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        message = f"🏡 Боғ ўчирилди 🗑\n🏷 {self.name}"
        Telegram.send_log(message, app_button=True)


# Gardener Models
class Gardener(BasePerson):
    debt = None
    landing = None
    class Meta:
        verbose_name = "Bog'bon "
        verbose_name_plural = "Bog'bonlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.pk is None:
            message = f"👨‍🌾 Янги боғбон қўшилди 🆕\n👨🏻‍🌾 {self.full_name} \n📞 {self.phone_number}"
            Telegram.send_log(message, app_button=True)
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        message = f"👨‍🌾 Боғбон ўчирилди 🗑\n👨🏻‍🌾 {self.full_name}"
        Telegram.send_log(message, app_button=True)


class GardenSalaryPayment(BaseModel):
    gardener = models.ForeignKey(Gardener, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="UZS")
    # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="garden_salary_payments")

    class Meta:
        verbose_name = "Oylik maosh"
        verbose_name_plural = "Oylik maoshlar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                old_payment = GardenSalaryPayment.objects.get(id=self.pk)

                Gardener.objects.filter(id=old_payment.gardener.id).update(
                    balance=F("balance") - convert_currency(
                        old_payment.currency_type, old_payment.gardener.currency_type, old_payment.amount
                    )
                )
                if self.gardener != old_payment.gardener:
                    raise ValidationError("It is not allowed to change gardener")

                User.objects.filter(id=old_payment.creator.id).update(
                    balance=F('balance') + convert_currency(
                        old_payment.currency_type, old_payment.creator.currency_type, old_payment.amount
                    )
                )
            else:
                message = f"💸 Ойлик маош\n🔣 Боғ\n📝 {self.gardener.full_name} га {self.amount} {self.currency_type} берилди\n👤 {self.creator.get_full_name()}\n➖ {self.amount} {self.currency_type}"
                Telegram.send_log(message, app_button=True)

            super().save(*args, **kwargs)

            Gardener.objects.filter(id=self.gardener.id).update(
                balance=F("balance") + convert_currency(
                    self.currency_type, self.gardener.currency_type, self.amount
                )
            )

            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') - convert_currency(
                    self.currency_type, self.creator.currency_type, self.amount
                )
            )

            if self.creator.role == "CEO":
                self.status = 'verified'

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            Gardener.objects.filter(id=self.gardener.id).update(
                balance=F("balance") - convert_currency(
                    self.currency_type, self.gardener.currency_type, self.amount
                )
            )

            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') + convert_currency(
                    self.currency_type, self.creator.currency_type, self.amount
                )
            )
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.gardener.full_name



