from django.db import models, transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError

from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE, TRANSFER_TYPE
from apps.common.utils import convert_currency
from apps.users.models import User


###############
## Just data ##
###############

###############
##  People   ##
###############

# Driver model
class Driver(BasePerson):
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    licence = models.CharField(max_length=30, null=True, blank=True)
    passport = models.CharField(max_length=30, null=True, blank=True)
    given_place = models.CharField(max_length=100, null=True, blank=True)
    given_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    landing = None
    debt = None

    class Meta:
        verbose_name = "Haydovchi "
        verbose_name_plural = "Haydovchilar "

    def __str__(self):
        return self.full_name


# Tenant model
class Tenant(BasePerson):
    trucks_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Ijarachi "
        verbose_name_plural = "Ijarachilar "

    def __str__(self):
        return self.full_name


class Contractor(BaseModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Shartnomachi firma nomi")
    inn = models.CharField(max_length=30, verbose_name="INN")
    phone_number = models.CharField(max_length=15, verbose_name="Telefon raqami")
    extra_phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Qo'shimcha telefon raqami")
    landing = models.FloatField(default=0, verbose_name="Qarzdorlik")
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPE, default="UZS", verbose_name="Valyuta turi")

    class Meta:
        verbose_name = "Shartnoma hamkori "
        verbose_name_plural = "Shartnoma hamkorlari "

    def __str__(self):
        return self.name


###############
##  Stuff    ##
###############

class Car(BaseModel):
    brand = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    state_number = models.CharField(max_length=20, unique=True)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20, null=True, blank=True)
    tech_passport = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    creator = None

    class Meta:
        verbose_name = "Mashina "
        verbose_name_plural = "Mashinalar "

    def save(self, *args, **kwargs):
        if self.tenant:
            if not self.pk:
                self.tenant.trucks_count -= 1
                self.tenant.save(update_fields=["trucks_count"])
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.tenant:
            if self.tenant.trucks_count and self.tenant.trucks_count > 0:
                self.tenant.trucks_count -= 1
                self.tenant.save(update_fields=["trucks_count"])
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.state_number

class Trailer(BaseModel):
    model = models.CharField(max_length=100, null=True, blank=True)
    state_number = models.CharField(max_length=20, unique=True)
    trailer_type = models.CharField(max_length=50, null=True, blank=True)
    dimensions = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.FloatField(null=True, blank=True)
    axle_count = models.PositiveSmallIntegerField(null=True, blank=True)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20, null=True, blank=True)
    tech_passport = models.CharField(max_length=20, unique=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Tirkama "
        verbose_name_plural = "Tirkamalar "

    def __str__(self):
        return self.state_number

    def save(self, *args, **kwargs):
        if self.creator.role == "CEO":
            self.status = 'verified'
        super().save(*args, **kwargs)


TIR_STATUS = (
    ('new', 'Yangi'),
    ('accepted', 'Qabul qilingan'),
    ('given', 'Berib yuborilgan'),
    ('waiting', 'Kutilmoqda'),
    ('submitted', 'Topshirilgan'),
)


class TIR(BaseModel):
    serial_number = models.CharField(max_length=30, verbose_name="TIR raqami")
    get_date = models.DateField(verbose_name="Olish sanasi")
    deadline = models.DateField(verbose_name="Muddati")
    status = models.CharField(max_length=20, choices=TIR_STATUS, default='new', verbose_name="Status")

    def __str__(self):
        return str(self.serial_number)

    class Meta:
        verbose_name = "TIR "
        verbose_name_plural = "TIRlar "
        ordering = ["-created_at"]



class Company(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Kompaniya nomi")
    director = models.CharField(max_length=100, null=True, blank=True, verbose_name="Boshliq F.I.O")
    inn = models.CharField(max_length=30, verbose_name="INN", null=True, blank=True)
    xp = models.CharField(max_length=30, verbose_name="XP", null=True, blank=True)
    mfo = models.CharField(max_length=30, verbose_name="MFO", null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name="Telefon raqami")
    email = models.CharField(max_length=100, verbose_name="Email", null=True, blank=True)
    creator = None
    status = None

    class Meta:
        verbose_name = "Kompaniya "
        verbose_name_plural = "Kompaniyalar "

    def __str__(self):
        return self.name


###############
##  Actions  ##
###############


class Waybill(BaseModel):
    departure_date = models.DateField()
    arrival_date = models.DateField(null=True, blank=True)
    driver_1 = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_1")
    driver_2 = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_2")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return str(self.created_at)

    class Meta:
        verbose_name = "Putyovka "
        verbose_name_plural = "Putyovkalar "
        ordering = ['-created_at']


class TIRRecord(BaseModel):
    tir = models.OneToOneField(TIR, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="TIR")
    waybill = models.OneToOneField(Waybill, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Putyovka ")
    tir_get_date = models.DateField(verbose_name="TIRni olgan kun")
    tir_deadline = models.DateField(verbose_name="Topshirish muddati")
    is_returned = models.BooleanField(default='False', verbose_name="Holati")

    class Meta:
        verbose_name = "TIR yozuvi "
        verbose_name_plural = "TIR yozuvlari "
        ordering = ["-created_at"]

    def __str__(self):
        return self.tir.serial_number if self.tir else str(self.id)

    def save(self, *args, **kwargs):
        with transaction.atomic():

            if self.creator.role == "CEO":
                self.status = 'verified'

            super().save(*args, **kwargs)



CONTRACT_STATUS = (
    ('new', 'Yangi'),
    ('waiting', 'Kutilmoqda'),
    ('warning', 'Ogohlantirish'),
    ('accepted', 'Qabul qilingan'),
    ('given', 'Berib yuborilgan')
)

class ContractRecord(BaseModel):
    contract_number = models.CharField(max_length=50, verbose_name="Shartnoma raqami")
    date = models.DateField(verbose_name="Shartnoma sanasi")
    invoice_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="Faktura raqami")
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField(null=True)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="UZS")
    remaining = models.FloatField(null=True)

    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default='new', verbose_name="Status")

    class Meta:
        verbose_name = "Shartnoma "
        verbose_name_plural = "Shartnomalar "

    def __str__(self):
        return self.contract_number

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                pass

            if self.contractor is None:
                raise ValueError("Contractor majburiy ravishda kiritilishi kerak.")

            if self.creator.role == "CEO":
                self.status = 'verified'

            super().save(*args, **kwargs)

            self.contractor.landing += self.amount
            self.contractor.save(update_fields=["landing"])

            # if self.tenant:
            #     self.tenant.debt += self.amount


class ContractCars(BaseModel):
    contract = models.ForeignKey(ContractRecord, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.SET_NULL, null=True, blank=True)
    status = None
    creator = None

    class Meta:
        verbose_name = "Shartnoma putyovkasi "
        verbose_name_plural = "Shartnoma putyovkalari "

    def __str__(self):
        return self.contract.contract_number


class ContractIncome(BaseModel):
    contract = models.ForeignKey(ContractRecord, on_delete=models.CASCADE)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="USD")
    date = models.DateField()
    bank_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Shartnoma to'lovi "
        verbose_name_plural = "Shartnoma to'lovlari "
        ordering = ["-created_at"]

    def __str__(self):
        return self.contract.contract_number



class CarExpense(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default='USD')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salary_payments_logistic")

    class Meta:
        verbose_name = "Mashina harajati "
        verbose_name_plural = "Mashina harajatlari "
        ordering = ['-created_at']

    # def save(self, *args, **kwargs):
    #     with transaction.atomic():
    #
    #         super().save(*args, **kwargs)

    def __str__(self):
        if self.car and self.trailer:
            return self.car.state_number, self.trailer.state_number
        elif self.car:
            return self.car.state_number
        elif self.trailer:
            return self.trailer.state_number
        return str(self.id)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = CarExpense.objects.get(id=self.pk)
                converted_amount = convert_currency(prev.currency_type, "UZS", prev.amount)
                User.objects.filter(id=prev.creator.id).update(balance=F('balance') + converted_amount)

                # old_amount = old_expense.amount
                # if self.currency_type != old_expense.currency_type:
                #     valid_currencies = ("USD", "UZS")
                #     if old_expense.currency_type in valid_currencies and self.currency_type in valid_currencies:
                #         old_amount = convert_currency(old_expense.currency_type, self.currency_type, old_amount)
                # if self.amount != old_expense.amount:
                #     if self.car:
                #         self.car.landing += old_amount
                #         self.car.save()
                #     if self.trailer:
                #         self.trailer.landing += old_amount
                #         self.trailer.save()
            # if self.car != old_expense.car:
            #     raise ValidationError("It is not allowed to change car")
            # if self.trailer != old_expense.trailer:
            #     raise ValidationError("It is not allowed to change trailer")
            # converted_amount = self.amount
            # if self.car:
            #     if self.car.currency_type == self.currency_type:
            #         valid_currencies = ("USD", "UZS")
            #         if self.car.currency_type in valid_currencies and self.currency_type in valid_currencies:
            #             converted_amount = convert_currency(self.currency_type, self.car.currency_type, self.amount)
            #         else:
            #             raise ValidationError("Invalid currency type")
            #     self.car.landing -= converted_amount
            #     self.car.save()
            # if self.trailer:
            #     if self.trailer.currency_type == self.currency_type:
            #         valid_currencies = ("USD", "UZS")
            #         if self.trailer.currency_type in valid_currencies and self.currency_type in valid_currencies:
            #             converted_amount = convert_currency(self.currency_type, self.trailer.currency_type, self.amount)
            #         else:
            #             raise ValidationError("Invalid currency type")
            #     self.trailer.landing -= converted_amount
            #     self.trailer.save()
            if self.creator.role == "CEO":
                self.status = 'verified'
            super().save(*args, **kwargs)

            converted_amount = convert_currency(self.currency_type, "UZS", self.amount)
            User.objects.filter(id=self.creator.id).update(balance=F('balance') + converted_amount)


class SalaryPayment(BaseModel):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="USD")

    class Meta:
        verbose_name = "Haydovchi maoshi "
        verbose_name_plural = "Haydovchilar maoshlari "
        ordering = ["-created_at"]

    def __str__(self):
        if self.driver:
            return f"{self.driver.full_name} - {self.amount}"
        elif self.description:
            return self.description
        return str(self.id)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                prev = SalaryPayment.objects.get(id=self.pk)
                converted_amount = convert_currency(prev.currency_type, "UZS", prev.amount)
                User.objects.filter(id=prev.creator.id).update(balance=F('balance') + converted_amount)

            if self.creator.role == "CEO":
                self.status = 'verified'

            super().save(*args, **kwargs)

            converted_amount = convert_currency(self.currency_type, "UZS", self.amount)
            User.objects.filter(id=self.creator.id).update(balance=F('balance') - converted_amount)


#
# TRANSIT_STATUS_CHOICES = (
#     ('new', 'Yangi'),
#     ('left', 'Yuborilgan'),
#     ('arrived', 'Qaytib kelgan'),
#     ('pending', 'To\'lov kutilyapti'),
#     ('finished', 'Yakunlangan')
# )
#
# class Transit(models.Model):
#     car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
#     trailer = models.ForeignKey(Trailer, on_delete=models.SET_NULL, null=True)
#     driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
#     leaving_contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, related_name='leaving_transits')
#     leaving_amount = models.FloatField(null=True, blank=True)
#     leaving_currency = models.CharField(max_length=20, choices=CURRENCY_TYPE)
#     leaving_date = models.DateTimeField(null=True, blank=True)
#     arrival_contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, related_name='arrival_transits')
#     arrival_amount = models.FloatField(null=True, blank=True)
#     arrival_currency = models.CharField(max_length=20, choices=CURRENCY_TYPE)
#     arrival_date = models.DateTimeField(null=True, blank=True)
#     driver_fee = models.FloatField(null=True, blank=True)
#     fee_currency = models.CharField(max_length=20, choices=CURRENCY_TYPE)
#     status = models.CharField(max_length=50, choices=TRANSIT_STATUS_CHOICES, default='new')
#     remainder = models.FloatField(default=0)
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
#
#     class Meta:
#         verbose_name = "Qatnov "
#         verbose_name_plural = "Qatnovlar "
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if self.pk:
#                 pass
#
#
#             if self.leaving_amount and self.arrival_amount:
#                 if self.leaving_currency == self.arrival_currency:
#                     self.remainder = self.leaving_amount + self.arrival_amount
#                 else:
#                     self.remainder = self.leaving_amount + convert_currency(self.arrival_currency, self.leaving_currency, self.arrival_amount)
#                 self.remainder = self.leaving_amount
#             elif self.leaving_amount:
#                 self.remainder = self.leaving_amount
#             elif self.arrival_amount:
#                 self.remainder = self.arrival_amount
#
#             if self.status == "finished":
#                 converted_driver_fee = self.driver_fee
#                 if self.driver.currency_type != self.fee_currency:
#                     converted_driver_fee = convert_currency(self.driver.currency_type, self.fee_currency, self.driver_fee)
#                 self.driver.balance += converted_driver_fee
#                 self.driver.save(update_fields=["balance"])
#
#             super().save(*args, **kwargs)
#
#     def __str__(self):
#         if self.driver and self.car and self.leaving_date:
#             return f"{self.driver.full_name} | {self.car.state_number} | {self.leaving_date}"
#         return str(self.id)
#
#
# class TransitExpense(BaseModel):
#     transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, null=True, blank=False)
#     reason = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)
#     amount = models.FloatField()
#     transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE, default="cash")
#     currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="USD")
#
#     class Meta:
#         verbose_name = "Qatnov xarajati "
#         verbose_name_plural = "Qatnov xarajatlari "
#         ordering = ["-created_at"]
#
#     def __str__(self):
#         if self.transit:
#             return f"{self.transit.id} | {self.reason}"
#         return self.reason
#
# REASON_CHOICES = (
#     ('leaving', 'Ketish uchun'),
#     ('arrival', 'Qaytish uchun'),
#     ('other', 'Boshqa')
# )
#
# class TransitIncome(BaseModel):
#     transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, null=True, blank=False)
#     reason = models.CharField(max_length=255, choices=REASON_CHOICES)
#     description = models.TextField(null=True, blank=True)
#     amount = models.FloatField()
#     transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE, default="transfer")
#     currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="USD")
#
#     class Meta:
#         verbose_name = "Qatnov kirimi "
#         verbose_name_plural = "Qatnov kirimlari "
#         ordering = ["-created_at"]
#
#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             if self.pk:
#                 pass
#
#             converted_amount = self.amount
#             if self.reason == "leaving":
#                 pass
#             if self.transit.leaving_currency != self.currency_type:
#                 self.transit.remainder -= convert_currency(self.currency_type, self.transit.leaving_currency, self.amount)
#
#             else:
#                 raise ValidationError("Reason should be one of the following: 'leaving', 'arrival' or 'other'")
#
#             if self.creator.role == "CEO":
#                 self.status = 'verified'
#
#             super().save(*args, **kwargs)
#
#     def __str__(self):
#         if self.transit:
#             return f"{self.transit.id} | {self.reason}"
#         return self.reason
