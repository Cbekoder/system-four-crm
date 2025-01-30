from django.db import models
from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE
from apps.main.models import Expense, Section,Income
from apps.common.utils import convert_currency

class Gardener(BasePerson):
    class Meta:
        verbose_name = "Bog'bon "
        verbose_name_plural = "Bog'bonlar "
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class SalaryPayment(BaseModel):
    gardener = models.ForeignKey(Gardener, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="UZS")

    class Meta:
        verbose_name = "Oylik maosh"
        verbose_name_plural = "Oylik maoshlar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.amount = convert_currency(self.currency_type, "UZS", self.amount)
        # Agar balans yangilanishi kerak bo'lsa
        if self.gardener:
            # Agar bu yangi obyekt bo'lsa, yangi balansni qo'shish
            if not self.pk:
                self.gardener.balance += self.amount
            # Agar bu mavjud obyekt bo'lsa, eski miqdorni chiqarib, yangi miqdorni qo'shish
            else:
                old_payment = SalaryPayment.objects.get(id=self.pk)
                self.gardener.balance += (self.amount - old_payment.amount)

            # Balansni saqlash
            self.gardener.save()

        # Aslida obyektni saqlash
        super().save(*args, **kwargs)

    def __str__(self):
        return self.gardener.full_name

class GardenIncome(Income):

    def __str__(self):
        return self.description[:50]

    class Meta:
        verbose_name = "Kirim "
        verbose_name_plural = "Kirimlar "
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.section:
            garden_section, _ = Section.objects.get_or_create(name="Bog'")
            self.section = garden_section
        super().save(*args, **kwargs)



class GardenExpense(Expense):
    class Meta:
        proxy = False
        verbose_name = "Chiqim "
        verbose_name_plural = "Chiqimlar "
        ordering = ['-created_at']

    # def save(self, *args, **kwargs):
    #     if not self.section:
    #         garden_section, _ = Section.objects.get_or_create(name="Bog'")
    #         self.section = garden_section
    #     super().save(*args, **kwargs)


