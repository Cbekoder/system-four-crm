from django.contrib import admin
from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, SalaryPayment, Contract,
    Transit, TransitExpense, TransitIncome, TIRRecord
)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number")
    search_fields = ("first_name", "last_name", "phone_number")


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number", "trucks_count")
    search_fields = ("first_name", "last_name", "phone_number")


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ("name", "inn", "phone_number")
    search_fields = ("name", "inn", "phone_number")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "state_number", "year", "color", "is_active", "tenant")
    search_fields = ("brand", "model", "state_number")
    list_filter = ("is_active", "year", "tenant")


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ("model", "state_number", "year", "color", "car")
    search_fields = ("model", "state_number")


@admin.register(CarExpense)
class CarExpenseAdmin(admin.ModelAdmin):
    list_display = ("car", "trailer", "reason", "amount", "currency_type", "created_at")
    search_fields = ("reason",)
    list_filter = ("currency_type", "created_at")


@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ("driver", "amount", "currency_type", "created_at")
    search_fields = ("driver__first_name", "driver__last_name")
    list_filter = ("currency_type", "created_at")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_id", "contractor")
    search_fields = ("contract_id", "contractor__first_name", "contractor__last_name")


@admin.register(Transit)
class TransitAdmin(admin.ModelAdmin):
    list_display = ("car", "driver", "leaving_contract", "leaving_date", "arrival_contract", "arrival_date", "status")
    search_fields = ("car__state_number", "driver__first_name", "driver__last_name")
    list_filter = ("status", "leaving_date", "arrival_date")


@admin.register(TransitExpense)
class TransitExpenseAdmin(admin.ModelAdmin):
    list_display = ("transit", "reason", "amount", "currency_type", "created_at")
    search_fields = ("reason", "transit__id")
    list_filter = ("currency_type", "created_at")


@admin.register(TransitIncome)
class TransitIncomeAdmin(admin.ModelAdmin):
    list_display = ("transit", "reason", "amount", "currency_type", "created_at")
    search_fields = ("reason", "transit__id")
    list_filter = ("currency_type", "created_at")


@admin.register(TIRRecord)
class TirSellingAdmin(admin.ModelAdmin):
    list_display = ("tir", "driver", "car", "trailer", "created_at")
    search_fields = ("tir", "driver__first_name", "driver__last_name", "car", "trailer")