from django.db import models, transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE
from apps.common.services.logging import Telegram

from apps.common.utils import convert_currency
from apps.main.models import Expense
from apps.users.models import User


# Worker Model
class Worker(BasePerson):
    debt = None
    landing = None

    class Meta:
        verbose_name = "Ishchi"
        verbose_name_plural = "Ishchilar"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name if self.full_name else str(self.id)

    def save(self, *args, **kwargs):
        if self.pk is None:
            message = f"🏭 Янги ишчи қўшилди 🆕\n👨🏼‍🏭 {self.full_name} \n📞 {self.phone_number}"
            Telegram.send_log(message, app_button=True)
        super().save(*args, **kwargs)


# Raw Material
class RawMaterial(BaseModel):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    description = models.TextField(null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Xomashyo "
        verbose_name_plural = "Xomashyolar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# Basket Model
class Basket(BaseModel):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    weight = models.FloatField()
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    per_worker_fee = models.FloatField()
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Savat "
        verbose_name_plural = "Savatlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# User Daily Work Model
class UserDailyWork(BaseModel):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Kunlik ish"
        verbose_name_plural = "Kunlik ishlar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            related_basket_counts = UserBasketCount.objects.filter(user_daily_work=self.id)

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

                Basket.objects.filter(id=prev.basket.id).update(quantity=F('quantity') - prev.quantity)
                # prev.basket.quantity = F('quantity') - prev.quantity
                # prev.basket.save(update_fields=['quantity'])
                # prev.basket.refresh_from_db()

                UserDailyWork.objects.filter(id=prev.user_daily_work.id).update(
                    amount=F('amount') - float(prev.quantity * prev.basket.per_worker_fee))
                # prev.user_daily_work.amount = F('amount') - float(prev.quantity * prev.basket.per_worker_fee)
                # prev.user_daily_work.save(update_fields=['amount'])
                # prev.user_daily_work.refresh_from_db()

                Worker.objects.filter(id=prev.user_daily_work.worker.id).update(
                    balance=F('balance') - convert_currency("UZS", prev.user_daily_work.worker.currency_type,
                                                            float(prev.quantity * prev.basket.per_worker_fee)))
                # prev.user_daily_work.worker.balance = F('balance') - float(prev.quantity * prev.basket.per_worker_fee)
                # prev.user_daily_work.worker.save(update_fields=['balance'])
                # prev.user_daily_work.worker.refresh_from_db()

                if prev.basket.raw_material:
                    RawMaterial.objects.filter(id=prev.basket.id).update(
                        weight=F('weight') + (prev.basket.weight / 1000) * prev.quantity)
                else:
                    last_raw = RawMaterial.objects.last()
                    RawMaterial.objects.filter(id=last_raw.id).update(
                        weight=F('weight') + (last_raw.weight / 1000) * prev.quantity)
                # raw_material.weight+=((prev.basket.weight)/1000)*prev.quantity
                # raw_material.save(update_fields=['weight'])

            super().save(*args, **kwargs)

            Basket.objects.filter(id=self.basket.id).update(quantity=F('quantity') + self.quantity)
            # self.basket.quantity = F('quantity') + self.quantity
            # self.basket.save(update_fields=['quantity'])
            # self.basket.refresh_from_db()

            Worker.objects.filter(id=self.user_daily_work.worker.id).update(
                balance=F('balance') + convert_currency("UZS", self.user_daily_work.worker.currency_type,
                                                        float(self.quantity * self.basket.per_worker_fee)))
            # self.user_daily_work.worker.balance = F('balance') + float(self.quantity * self.basket.per_worker_fee)
            # self.user_daily_work.worker.save(update_fields=['balance'])
            # self.user_daily_work.worker.refresh_from_db()

            UserDailyWork.objects.filter(id=self.user_daily_work.id).update(
                amount=F('amount') + float(self.quantity * self.basket.per_worker_fee))
            # self.user_daily_work.amount = F('amount') + float(self.quantity * self.basket.per_worker_fee)
            # self.user_daily_work.save(update_fields=['amount'])
            # self.user_daily_work.refresh_from_db()

            if self.basket.raw_material:
                RawMaterial.objects.filter(id=self.basket.id).update(
                    weight=F('weight') - (self.basket.weight / 1000) * self.quantity)
            else:
                last_raw = RawMaterial.objects.last()
                RawMaterial.objects.filter(id=last_raw.id).update(
                    weight=F('weight') - (last_raw.weight / 1000) * self.quantity)
            # raw_material.weight-=((self.basket.weight)/1000)*self.quantity
            # raw_material.save(update_fields=['weight'])
            # print(raw_material.weight)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            Basket.objects.filter(id=self.basket.id).update(quantity=F('quantity') - self.quantity)
            # self.basket.quantity = F('quantity') - self.quantity
            # self.basket.save(update_fields=['quantity'])

            Worker.objects.filter(id=self.user_daily_work.worker.id).update(
                balance=F('balance') - convert_currency("UZS", self.user_daily_work.worker.currency_type,
                                                        float(self.quantity * self.basket.per_worker_fee)))
            # self.user_daily_work.worker.balance = F('balance') - self.quantity * self.basket.per_worker_fee
            # self.user_daily_work.worker.save(update_fields=['balance'])

            UserDailyWork.objects.filter(id=self.user_daily_work).update(
                amount=F('amount') - float(self.quantity * self.basket.per_worker_fee))
            # self.user_daily_work.amount = F('amount') - (self.quantity * self.basket.per_worker_fee)
            # self.user_daily_work.save(update_fields=['amount'])

            if self.basket.raw_material:
                RawMaterial.objects.filter(id=self.basket.id).update(
                    weight=F('weight') + (self.basket.weight / 1000) * self.quantity)
            else:
                last_raw = RawMaterial.objects.last()
                RawMaterial.objects.filter(id=last_raw.id).update(
                    weight=F('weight') + (last_raw.weight / 1000) * self.quantity)
            # raw_material = RawMaterial.objects.all().first()
            #
            # raw_material.weight += ((self.basket.weight) / 1000) * self.quantity
            # raw_material.save(update_fields=['weight'])

            super().delete(*args, **kwargs)


# Supplier Model
class Supplier(BaseModel):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    extra_phone_number = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Ta'minotchi "
        verbose_name_plural = "Ta'minotchilar "
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# Raw Material History
class RawMaterialHistory(BaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    date = models.DateField()

    class Meta:
        verbose_name = "Xomashyo tarixi "
        verbose_name_plural = "Xomashyo tarixi "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = RawMaterialHistory.objects.get(pk=self.pk)

                RawMaterial.objects.filter(id=prev.raw_material.id).update(weight=F('weight') - prev.weight)
                # prev.raw_material.weight = F('weight') - prev.weight
                # prev.raw_material.save(update_fields=['weight'])
                # prev.raw_material.refresh_from_db()

                User.objects.filter(id=prev.creator.id).update(
                    balance=F('balance') + convert_currency(prev.currency_type, prev.creator.currency_type,
                                                            prev.amount))

            super().save(*args, **kwargs)

            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount))
            # if self.raw_material.currency_type != self.currency_type:
            #     self.amount = convert_currency(self.raw_material.currency_type, self.currency_type, self.amount)

            RawMaterial.objects.filter(id=self.raw_material.id).update(weight=F('weight') + self.weight)
            # self.raw_material.weight = F('weight') + self.weight
            # self.raw_material.save(update_fields=['weight'])
            # self.raw_material.refresh_from_db()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            RawMaterial.objects.filter(id=self.raw_material.id).update(weight=F('weight') - self.weight)

            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount))

            super().delete(*args, **kwargs)

    def __str__(self):
        return self.supplier.name


# Client Models
class Client(BasePerson):
    class Meta:
        verbose_name = "Mijoz "
        verbose_name_plural = "Mijozlar "

        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class PayDebt(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=15, choices=CURRENCY_TYPE)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    class Meta:

        verbose_name = "Qarz to'lash "

        verbose_name_plural = "Qarzlar to'lash "

        ordering = ['-date']

    def save(self, *args, **kwargs):

        if self.pk:
            prev_pay_debt = PayDebt.objects.get(pk=self.pk)

            prev_amount = prev_pay_debt.amount

            prev_amount = convert_currency(prev_pay_debt.currency_type, prev_pay_debt.client.currency_type, prev_amount)

            self.client.debt += prev_amount

        amount = convert_currency(self.currency_type, self.client.currency_type, self.amount)

        if amount > self.client.debt:
            raise ValidationError("To‘lov miqdori mijoz qarzidan ko‘p bo‘lishi mumkin emas!")

        self.client.debt -= amount

        self.client.save(update_fields=['debt'])

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        amount = convert_currency(self.currency_type, self.client.currency_type, self.amount)

        self.client.debt += amount

        self.client.save(update_fields=['debt'])

        super().delete(*args, **kwargs)


class Sale(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_debt = models.BooleanField(default=False)
    date = models.DateField()

    class Meta:
        verbose_name = "Sotuv"
        verbose_name_plural = "Sotuvlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sotuv #{self.pk} | {self.client.full_name if self.client is not None else 'Noma’lum'}"

    @property
    def total_amount(self):
        return sum(item.amount for item in self.sale_items.all())

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.sale_items.all())

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                existing_items = {item.id: item for item in self.sale_items.all()}
                new_items_data = {item['id']: item for item in kwargs.pop('sale_items', []) if 'id' in item}

                items_to_delete = [item for item_id, item in existing_items.items() if item_id not in new_items_data]
                for item in items_to_delete:
                    item.delete()
            super().save(*args, **kwargs)
            self.refresh_from_db()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            for item in self.sale_items.all():
                item.delete()
            super().delete(*args, **kwargs)


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    amount = models.FloatField(default=0)

    class Meta:
        verbose_name = "Sotuv mahsuloti"
        verbose_name_plural = "Sotuv mahsulotlari"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = SaleItem.objects.get(pk=self.pk)

                Basket.objects.filter(id=prev.basket.id).update(
                    quantity=F('quantity') + prev.quantity
                )

                if prev.sale.is_debt:
                    if prev.sale.client:
                        Client.objects.filter(id=prev.sale.client.id).update(
                            debt=F('debt') - convert_currency("UZS", prev.sale.client.currency_type, prev.amount)
                        )
                    else:
                        raise ValidationError({"error": "Агар қарзга берилаётган бўлса, Клиент мажбурий бўлиши керак!"})
                else:
                    User.objects.filter(prev.sale.creator.id).update(
                        balance=F('balance') - convert_currency("UZS", prev.sale.creator.currency_type, prev.amount)
                    )

            if not self.amount:
                self.amount = self.quantity * self.basket.price

            super().save(*args, **kwargs)

            Basket.objects.filter(id=self.basket.id).update(
                quantity=F('quantity') - self.quantity
            )

            if self.sale.is_debt:
                if self.sale.client:
                    Client.objects.filter(id=self.sale.client.id).update(
                        debt=F('debt') + convert_currency("UZS", self.sale.client.currency_type, self.amount)
                    )
                else:
                    raise ValidationError({"error": "Агар қарзга берилаётган бўлса, Клиент мажбурий бўлиши керак!"})
            else:
                User.objects.filter(id=self.sale.creator.id).update(
                    balance=F('balance') + convert_currency("UZS", self.sale.creator.currency_type, self.amount)
                )



    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.basket.quantity = F('quantity') + self.quantity
            self.basket.save(update_fields=['quantity'])
            super().delete(*args, **kwargs)
            if self.sale.is_debt and self.sale.client:
                self.sale.client.debt = F('debt') - self.amount
                self.sale.client.save(update_fields=['debt'])

    def __str__(self):
        return f"{self.sale.client.name if self.sale.client is not None else 'Noma’lum'} - {self.basket.name}"



class SalaryPayment(BaseModel):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salary_payments_factory")
    date = models.DateField()

    class Meta:
        verbose_name = "Oylik maosh "
        verbose_name_plural = "Oylik maosh "
        ordering = ['-created_at']

    def __str__(self):
        return self.worker.first_name

    def save(self, *args, **kwargs):

        if self.pk:
            prev = SalaryPayment.objects.get(pk=self.pk)

            Worker.objects.filter(id=prev.worker.id).update(
                balance=F('balance') + convert_currency(prev.currency_type, prev.worker.currency_type, prev.amount))

            User.objects.filter(id=prev.creator.id).update(
                balance=F('balance') + convert_currency(prev.currency_type, prev.creator.currency_type, prev.amount))

        super().save(*args, **kwargs)

        Worker.objects.filter(id=self.worker.id).update(
            balance=F('balance') - convert_currency(self.currency_type, self.worker.currency_type, self.amount))

        User.objects.filter(id=self.creator.id).update(
            balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount))

    def delete(self, *args, **kwargs):
        Worker.objects.filter(id=self.worker.id).update(
            balance=F('balance') - convert_currency(self.currency_type, self.worker.currency_type, self.amount))

        User.objects.filter(id=self.creator.id).update(
            balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount))

        super().delete(*args, **kwargs)
