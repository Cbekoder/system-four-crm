from datetime import timezone, datetime

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


                Worker.objects.filter(id=prev.user_daily_work.worker.id).update(
                    balance=F('balance') - convert_currency("UZS", prev.user_daily_work.worker.currency_type,
                                                            float(prev.quantity * prev.basket.per_worker_fee)))

                if prev.basket.raw_material:
                    RawMaterial.objects.filter(id=prev.basket.raw_material.id).update(
                        weight=F('weight') + (prev.basket.weight / 1000) * prev.quantity)
                else:
                    last_raw = RawMaterial.objects.last()
                    RawMaterial.objects.filter(id=last_raw.id).update(
                        weight=F('weight') + (last_raw.weight / 1000) * prev.quantity)

            super().save(*args, **kwargs)

            Basket.objects.filter(id=self.basket.id).update(quantity=F('quantity') + self.quantity)

            Worker.objects.filter(id=self.user_daily_work.worker.id).update(
                balance=F('balance') + convert_currency("UZS", self.user_daily_work.worker.currency_type,
                                                        float(self.quantity * self.basket.per_worker_fee)))


            UserDailyWork.objects.filter(id=self.user_daily_work.id).update(
                amount=F('amount') + float(self.quantity * self.basket.per_worker_fee))

            if self.basket.raw_material:
                RawMaterial.objects.filter(id=self.basket.raw_material.id).update(
                    weight=F('weight') - (self.basket.weight / 1000) * self.quantity)
            else:
                last_raw = RawMaterial.objects.last()
                RawMaterial.objects.filter(id=last_raw.id).update(
                    weight=F('weight') - (last_raw.weight / 1000) * self.quantity)

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

            UserDailyWork.objects.filter(id=self.user_daily_work.id).update(
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
    landing = None
    balance = None

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
    date = models.DateField(default=datetime.now)

    class Meta:
        verbose_name = "Qarz to'lash "
        verbose_name_plural = "Qarzlar to'lash "
        ordering = ['-date']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = PayDebt.objects.get(pk=self.pk)

                Client.objects.filter(id=prev.client.id).update(
                    debt=F("debt") + convert_currency(prev.currency_type, prev.client.currency_type, prev.amount))

                User.objects.filter(id=prev.creator.id).update(
                    balance=F('balance') - convert_currency(prev.currency_type, prev.creator.currency_type, prev.amount))

            super().save(*args, **kwargs)

            Client.objects.filter(id=self.client.id).update(
                debt=F("debt") - convert_currency(self.currency_type, self.client.currency_type, self.amount)
            )

            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') + convert_currency(self.currency_type, self.creator.currency_type, self.amount))

    def delete(self, *args, **kwargs):

        Client.objects.filter(id=self.client.id).update(
            debt=F("debt") + convert_currency(self.currency_type, self.client.currency_type, self.amount))

        User.objects.filter(id=self.creator.id).update(
            balance=F('balance') - convert_currency(self.currency_type, self.creator.currency_type, self.amount))

        super().delete(*args, **kwargs)


class Sale(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    payed_amount= models.FloatField(default=0)
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
    def debt_amount(self):
        return self.total_amount - self.payed_amount

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.sale_items.all())

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self.pk is None  # Yangi sotuvmi yoki mavjudini o'zgartiryapmizmi?

            super().save(*args, **kwargs)  # Sotuvni saqlaymiz

            self.refresh_from_db()  # `sale_items` yangilanishi uchun

            # 1️⃣ **Oldingi qarzni olib tashlash**
            prev = Sale.objects.filter(pk=self.pk).first()
            prev_debt_amount = prev.debt_amount if prev else 0

            if self.pk:

                print("prev ichi 1", prev_debt_amount, self.client.debt)
                Client.objects.filter(id=self.client.id).update(
                    debt=F('debt') - convert_currency("UZS", self.client.currency_type, prev_debt_amount)
                )
                print("prev ichi 2", prev_debt_amount, self.client.debt)
                # self.client.refresh_from_db()  # Clientni yangilaymiz
                print("prev ichi 3", prev_debt_amount, self.client.debt)

            # 2️⃣ **Yangi `total_amount`ni hisoblash**
            total_amount = sum(item.amount for item in self.sale_items.all())
            debt_amount = total_amount - self.payed_amount
            converted_debt = convert_currency("UZS", self.client.currency_type, debt_amount)

            # 3️⃣ **Yangi qarzni qo‘shish**
            if self.client:
                print(self.client.debt)  # **Debug qilish uchun**
                print(converted_debt)
                Client.objects.filter(id=self.client.id).update(debt=F('debt') + converted_debt)
                # self.client.refresh_from_db()  # Yangilangan qiymatni olish
                print(self.client.debt)      # **Yangilangan debt qiymatini tekshirish**

            # **Clientni save qilish** (client objectni yangilab yuborish)
            if self.client:
                self.client.save()  # **Bu yerda clientni yana saqlashni qo'shamiz**

            # 4️⃣ **Foydalanuvchi balansini yangilash**
            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') + convert_currency("UZS", self.creator.currency_type, self.payed_amount)
            )

            # ✅ **Chop etish (debug qilish uchun)**
            print(f"Total Amount: {total_amount}")
            print(f"Payed Amount: {self.payed_amount}")
            print(f"Debt Amount (Calculated): {debt_amount}")
            print(f"Previous Debt Amount: {prev_debt_amount}")
            print(
                f"Updated Client Debt: {self.client.debt}")  # **Bu joyda noto‘g‘ri bo‘lsa, `refresh_from_db()` ishlamayapti**

    def delete(self, *args, **kwargs):
        with transaction.atomic():

            Client.objects.filter(id=self.client.id).update(
                debt=F('debt') - convert_currency("UZS", self.client.currency_type, self.debt_amount)
            )
            User.objects.filter(id=self.creator.id).update(
                balance=F('balance') - convert_currency("UZS", self.creator.currency_type, self.payed_amount)
            )
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
                # Client.objects.filter(id=self.client.id).update(
                #     debt=F('debt') - convert_currency("UZS", self.client.currency_type, self.amount)
                # )

            # if self.sale.client:
            #     Client.objects.filter(id=self.sale.client.id).update(
            #         debt=F('debt') + convert_currency("UZS", self.sale.client.currency_type, self.amount)
            #     )
            #     print(Client.objects.filter(id=self.sale.client.id))
            #     print("item",self.amount,self.sale.client.debt)

            if not self.amount:
                self.amount = self.quantity * self.basket.price

            super().save(*args, **kwargs)

            self.sale.refresh_from_db()
            self.sale.save()

            Basket.objects.filter(id=self.basket.id).update(quantity=F('quantity') - self.quantity)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.basket.quantity = F('quantity') + self.quantity
            self.basket.save(update_fields=['quantity'])
            super().delete(*args, **kwargs)

            if self.sale.client:

                Client.objects.filter(id=self.sale.client.id).update(
                    debt=F('debt') - convert_currency("UZS", self.sale.client.currency_type, self.amount)
                )

            else:
                User.objects.filter(id=self.sale.creator.id).update(
                    balance=F('balance') - convert_currency("UZS", self.sale.creator.currency_type, self.amount)
                )

    def __str__(self):
        return f"{self.sale.client.full_name if self.sale.client is not None else 'Noma’lum'} - {self.basket.name}"



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
