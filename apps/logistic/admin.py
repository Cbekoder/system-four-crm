from django.contrib import admin
from .models import (
    Driver, Tenant, Contractor, Car, Trailer, CarExpense, LogisticSalaryPayment, TIRRecord, ContractRecord,
    # Contract, Transit, TransitExpense, TransitIncome,
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


@admin.register(LogisticSalaryPayment)
class LogisticSalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ("driver", "amount", "currency_type", "created_at")
    search_fields = ("driver__first_name", "driver__last_name")
    list_filter = ("currency_type", "created_at")


@admin.register(ContractRecord)
class ContractRecordAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'date', 'invoice_number', 'contractor', 'amount', 'currency_type', 'remaining', 'status')
    list_filter = ('status', 'currency_type', 'date')
    search_fields = ('contract_number', 'invoice_number', 'contractor__name')
    ordering = ('-date',)
