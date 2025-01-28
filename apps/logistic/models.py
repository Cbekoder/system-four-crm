from django.db import models
from apps.common.models import BaseModel, BasePerson, CURRENCY_TYPE, TRANSFER_TYPE

###############
## Just data ##
###############

###############
##  People   ##
###############
class Driver(BasePerson):
    class Meta:
        verbose_name = "Haydovchi"
        verbose_name_plural = "Haydovchi"

    def __str__(self):
        return self.full_name


class Tenant(BasePerson):
    trucks_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Ijarachi "
        verbose_name_plural = "Ijarachilar "

    def __str__(self):
        return self.full_name


class Contractor(BasePerson):
    balance = None

    class Meta:
        verbose_name = "Shartnoma hamkori "
        verbose_name_plural = "Shartnoma hamkorlari "

    def __str__(self):
        return self.full_name


###############
##  Staff    ##
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

    class Meta:
        verbose_name = "Mashina "
        verbose_name_plural = "Mashinalar "

    def __str__(self):
        return self.state_number

class Trailer(BaseModel):
    model = models.CharField(max_length=100, null=True, blank=True)
    state_number = models.CharField(max_length=20, unique=True)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20, null=True, blank=True)
    tech_passport = models.CharField(max_length=20, unique=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Tirkama "
        verbose_name_plural = "Tirkamalar "

    def __str__(self):
        return self.state_number

###############
##  Actions  ##
###############

class CarExpense(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default='USD')

    class Meta:
        verbose_name = "Mashina harajati "
        verbose_name_plural = "Mashina harajatlari "
        ordering = ['-created_at']

    def __str__(self):
        if self.car and self.trailer:
            return self.car.state_number, self.trailer.state_number
        elif self.car:
            return self.car.state_number
        elif self.trailer:
            return self.trailer.state_number
        return str(self.id)


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

class Contract(BaseModel):
    contract_id = models.CharField(max_length=50)
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = "Shartnoma "
        verbose_name_plural = "Shartnomalar "

    def __str__(self):
        return self.contract_id

STATUS_CHOICES = (
    ('new', 'Yangi'),
    ('left', 'Yuborilgan'),
    ('arrived', 'Qaytib kelgan'),
    ('pending', 'To\'lov kutilyapti'),
    ('finished', 'Yakunlangan')
)

class Transit(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    leaving_contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, related_name='leaving_transits')
    leaving_amount = models.FloatField(null=True, blank=True)
    leaving_date = models.DateTimeField(null=True, blank=True)
    arrival_contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, related_name='arrival_transits')
    arrival_amount = models.FloatField(null=True, blank=True)
    arrival_date = models.DateTimeField(null=True, blank=True)
    driver_fee = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')

    class Meta:
        verbose_name = "Qatnov "
        verbose_name_plural = "Qatnovlar "

    def __str__(self):
        if self.driver and self.car and self.leaving_date:
            return f"{self.driver.full_name} | {self.car.state_number} | {self.leaving_date}"
        return str(self.id)


class TransitExpense(BaseModel):
    transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, null=True, blank=False)
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE, default="cash")
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="USD")

    class Meta:
        verbose_name = "Qatnov xarajati "
        verbose_name_plural = "Qatnov xarajatlari "
        ordering = ["-created_at"]

    def __str__(self):
        if self.transit:
            return f"{self.transit.id} | {self.reason}"
        return self.reason

class TransitIncome(BaseModel):
    transit = models.ForeignKey(Transit, on_delete=models.SET_NULL, null=True, blank=False)
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE, default="cash")
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPE, default="USD")

    class Meta:
        verbose_name = "Qatnov kirimi "
        verbose_name_plural = "Qatnov kirimlari "
        ordering = ["-created_at"]

    def __str__(self):
        if self.transit:
            return f"{self.transit.id} | {self.reason}"
        return self.reason




class TirSelling(BaseModel):
    tir_number = models.CharField(max_length=40, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=False)
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True)
