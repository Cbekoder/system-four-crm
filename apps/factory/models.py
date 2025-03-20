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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)


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

                prev.user_daily_work.amount = F('amount') - float(prev.quantity * prev.basket.per_worker_fee)
                prev.user_daily_work.save(update_fields=['amount'])
                prev.user_daily_work.refresh_from_db()

                prev.user_daily_work.worker.balance = F('balance') - float(prev.quantity * prev.basket.per_worker_fee)
                prev.user_daily_work.worker.save(update_fields=['balance'])
                prev.user_daily_work.worker.refresh_from_db()

            super().save(*args, **kwargs)

            self.basket.quantity = F('quantity') + self.quantity
            self.basket.save(update_fields=['quantity'])
            self.basket.refresh_from_db()

            self.user_daily_work.worker.balance = F('balance') + float(self.quantity * self.basket.per_worker_fee)
            self.user_daily_work.worker.save(update_fields=['balance'])
            self.user_daily_work.worker.refresh_from_db()

            self.user_daily_work.amount = F('amount') + float(self.quantity * self.basket.per_worker_fee)
            self.user_daily_work.save(update_fields=['amount'])
            self.user_daily_work.refresh_from_db()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.basket.quantity = F('quantity') - self.quantity
            self.basket.save(update_fields=['quantity'])

            self.user_daily_work.worker.balance = F('balance') - self.quantity * self.basket.per_worker_fee
            self.user_daily_work.worker.save(update_fields=['balance'])

            self.user_daily_work.amount = F('amount') - (self.quantity * self.basket.per_worker_fee)
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
    supplier = models.CharField(max_length=100, null=True, blank=True)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")

    class Meta:
        verbose_name = "Xomashyo tarixi "
        verbose_name_plural = "Xomashyo tarixi "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = RawMaterialHistory.objects.get(pk=self.pk)
                prev.raw_material.weight = F('weight') - prev.weight
                prev.raw_material.save(update_fields=['weight'])
                prev.raw_material.refresh_from_db()

            # if self.raw_material.currency_type != self.currency_type:
            #     self.amount = convert_currency(self.raw_material.currency_type, self.currency_type, self.amount)

            self.raw_material.weight = F('weight') + self.weight
            self.raw_material.save(update_fields=['weight'])
            self.raw_material.refresh_from_db()

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.raw_material.weight = F('weight') - self.weight
            self.raw_material.save(update_fields=['weight'])
            self.raw_material.refresh_from_db()

            super().delete(*args, **kwargs)

    def __str__(self):
        return self.supplier

class RawMaterialUsage(BaseModel):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    date=models.DateField(auto_now=True)


    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = RawMaterialUsage.objects.get(pk=self.pk)
                prev.raw_material.weight = F('weight') + prev.amount
                prev.raw_material.save(update_fields=['weight'])
                prev.raw_material.refresh_from_db()


            self.raw_material.weight = F('weight') - self.amount
            self.raw_material.save(update_fields=['weight'])
            self.raw_material.refresh_from_db()

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.raw_material.weight = F('weight') + self.amount
            self.raw_material.save(update_fields=['weight'])
            self.raw_material.refresh_from_db()

            super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Xomashyo ishlatilishi "
        verbose_name_plural = "Xomashyo ishlatilishi "
        ordering = ['-created_at']

class Client(BasePerson):
    class Meta:
        verbose_name = "Mijoz "
        verbose_name_plural = "Mijozlar "

        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


# class Sale(BaseModel):
#     client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     is_debt = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "Sotuv"
#         verbose_name_plural = "Sotuvlar"
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"Sotuv #{self.pk} | {self.client.name if self.client else 'Noma’lum'}"
#
#     @property
#     def total_amount(self):
#         return sum(item.amount for item in self.sale_items.all())
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             prev_items_dict = {}
#             if self.pk:
#                 prev_items_dict = {
#                     item.basket_id: item.quantity for item in self.sale_items.all()
#                 }
#
#             super().save(*args, **kwargs)
#
#             new_items = self.sale_items.all()
#             for item in new_items:
#                 prev_quantity = prev_items_dict.get(item.basket_id, 0)
#                 quantity_diff = item.quantity - prev_quantity
#
#                 item.basket.quantity = F('quantity') - quantity_diff
#                 item.basket.save(update_fields=['quantity'])
#
#             for basket_id, old_quantity in prev_items_dict.items():
#                 if basket_id not in [item.basket_id for item in new_items]:
#                     basket = Basket.objects.get(id=basket_id)
#                     basket.quantity = F('quantity') + old_quantity
#                     basket.save(update_fields=['quantity'])
#
#             if self.is_debt and self.client:
#                 self.client.debt = F('debt') + self.total_amount
#                 self.client.save(update_fields=['debt'])
#
#     def delete(self, *args, **kwargs):
#         with transaction.atomic():
#             for item in self.sale_items.all():
#                 item.basket.quantity = F('quantity') + item.quantity
#                 item.basket.save(update_fields=['quantity'])
#
#             if self.is_debt and self.client:
#                 self.client.debt = F('debt') - self.total_amount
#                 self.client.save(update_fields=['debt'])
#
#             super().delete(*args, **kwargs)
#
#
# class SaleItem(models.Model):
#     sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_items')
#     basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)
#     amount = models.FloatField(default=0)
#
#     class Meta:
#         verbose_name = "Sotuv mahsuloti"
#         verbose_name_plural = "Sotuv mahsulotlari"
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if self.pk:
#                 prev = SaleItem.objects.get(pk=self.pk)
#                 prev_quantity = prev.quantity
#
#                 # Eski mahsulotni qaytarish
#                 prev.basket.quantity = F('quantity') + prev_quantity
#                 prev.basket.save(update_fields=['quantity'])
#                 prev.basket.refresh_from_db()
#             else:
#                 prev_quantity = 0
#
#             if not self.amount:
#                 self.amount = self.quantity * self.basket.price
#
#             # Yangi mahsulot miqdorini hisoblash
#             quantity_diff = self.quantity - prev_quantity
#             self.basket.quantity = F('quantity') - quantity_diff
#             self.basket.save(update_fields=['quantity'])
#             self.basket.refresh_from_db()
#
#             super().save(*args, **kwargs)
#
#     def delete(self, *args, **kwargs):
#         with transaction.atomic():
#             self.basket.quantity = F('quantity') + self.quantity
#             self.basket.save(update_fields=['quantity'])
#
#             super().delete(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.sale.client.name if self.sale.client else 'Noma’lum'} - {self.basket.name}"


class Sale(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_debt = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sotuv"
        verbose_name_plural = "Sotuvlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sotuv #{self.pk} | {self.client.name if self.client else 'Noma’lum'}"

    @property
    def total_amount(self):
        return sum(item.amount for item in self.sale_items.all())

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                existing_items = {item.id: item for item in self.sale_items.all()}
                new_items_data = {item['id']: item for item in kwargs.pop('sale_items', []) if 'id' in item}


                items_to_delete = [item for item_id, item in existing_items.items() if item_id not in new_items_data]
                for item in items_to_delete:
                    item.delete()

            super().save(*args, **kwargs)

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
                prev_quantity = prev.quantity
                prev.basket.quantity = F('quantity') + prev_quantity
                prev.basket.save(update_fields=['quantity'])
                prev.basket.refresh_from_db()
            else:
                prev_quantity = 0

            if not self.amount:
                self.amount = self.quantity * self.basket.price

            quantity_diff = self.quantity - prev_quantity
            self.basket.quantity = F('quantity') - quantity_diff
            self.basket.save(update_fields=['quantity'])
            self.basket.refresh_from_db()

            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.basket.quantity = F('quantity') + self.quantity
            self.basket.save(update_fields=['quantity'])
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.sale.client.name if self.sale.client else 'Noma’lum'} - {self.basket.name}"



# class Sale(BaseModel):
#     basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
#     client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     quantity = models.IntegerField(default=0)
#     amount = models.FloatField(default=0)
#     currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
#     is_debt=models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "Sotuv "
#         verbose_name_plural = "Sotuvlar "
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return self.basket.name
#
#     def save(self, *args, **kwargs):
#         if self.pk:
#             prev=Sale.objects.get(pk=self.pk)
#             self.basket.quantity = F('quantity') + prev.quantity
#             self.basket.save(update_fields=['quantity'])
#         self.amount= self.quantity * self.basket.price
#         self.basket.quantity = F('quantity') - self.quantity
#         self.basket.save(update_fields=['quantity'])
#         super().save(*args, **kwargs)
#
#     def delete(self, *args, **kwargs):
#         self.basket.quantity = F('quantity') + self.quantity
#         self.basket.save(update_fields=['quantity'])
#         super().delete(*args, **kwargs)
#


class SalaryPayment(BaseModel):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    description = models.TextField(null=True, blank=True)
    creator=models.ForeignKey(User, on_delete=models.CASCADE,related_name="salary_payments_factory")

    class Meta:
        verbose_name = "Oylik maosh "
        verbose_name_plural = "Oylik maosh "
        ordering = ['-created_at']

    def __str__(self):
        return self.worker.first_name

    def save(self, *args, **kwargs):

        if self.pk:
            prev=SalaryPayment.objects.get(pk=self.pk)
            if prev.currency_type != self.worker.currency_type:
                prev.amount = convert_currency(prev.currency_type, self.worker.currency_type, prev.amount)
            self.worker.balance+=prev.amount
            old_expense = SalaryPayment.objects.get(id=self.pk)

            User.objects.filter(id=old_expense.creator.id).update(balance=F('balance') + old_expense.amount)

        if self.worker.currency_type != self.currency_type:
            amount = convert_currency(self.currency_type, self.worker.currency_type, self.amount)
            self.worker.balance-=amount
            self.worker.save()
        else:
            self.worker.balance -= self.amount
            self.worker.save()

        super().save(*args, **kwargs)

        User.objects.filter(id=self.creator.id).update(balance=F('balance') - self.amount)

    def delete(self, *args, **kwargs):
        if self.worker.currency_type != self.currency_type:

            amount = convert_currency(self.currency_type, self.worker.currency_type, self.amount)
            self.worker.balance += amount
            self.worker.save()
        else:
            self.worker.balance += self.amount
            self.worker.save()

        Expense.objects.filter(description__contains=f"| {self.id}").delete()

        User.objects.filter(id=self.creator.id).update(balance=F('balance') + self.amount)

        super().delete(*args, **kwargs)

