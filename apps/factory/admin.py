from django.contrib import admin
from .models import (
    Worker, RawMaterial, Basket, UserDailyWork, UserBasketCount,
    Supplier, RawMaterialHistory, Client, PayDebt, Sale, SaleItem,
    SalaryPayment
)

# Inline for UserBasketCount
class UserBasketCountInline(admin.TabularInline):
    model = UserBasketCount
    extra = 1
    fields = ('basket', 'quantity')
    readonly_fields = ()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "basket":
            kwargs["queryset"] = Basket.objects.all().order_by('id')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Inline for SaleItem
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ('basket', 'quantity', 'amount')
    autocomplete_fields = ['basket']

# Worker Admin
@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'created_at')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('created_at',)

# RawMaterial Admin
@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

# Basket Admin
@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'weight', 'quantity', 'price', 'per_worker_fee', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    autocomplete_fields = ['raw_material']

# UserDailyWork Admin
@admin.register(UserDailyWork)
class UserDailyWorkAdmin(admin.ModelAdmin):
    list_display = ('worker', 'amount', 'date', 'created_at')
    search_fields = ('worker__full_name',)
    list_filter = ('date', 'created_at')
    inlines = [UserBasketCountInline]
    autocomplete_fields = ['worker']

# Supplier Admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created_at')
    search_fields = ('name', 'phone_number')
    list_filter = ('created_at',)

# RawMaterialHistory Admin
@admin.register(RawMaterialHistory)
class RawMaterialHistoryAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'raw_material', 'weight', 'amount', 'date', 'created_at')
    search_fields = ('supplier__name', 'raw_material__name')
    list_filter = ('date', 'currency_type', 'created_at')
    autocomplete_fields = ['supplier', 'raw_material']

# Client Admin
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'debt', 'phone_number', 'created_at')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('created_at',)

# PayDebt Admin
@admin.register(PayDebt)
class PayDebtAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'currency_type', 'date', 'created_at')
    search_fields = ('client__full_name',)
    list_filter = ('currency_type', 'date', 'created_at')
    autocomplete_fields = ['client']

# Sale Admin
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('client', 'payed_amount', 'total_amount', 'debt_amount', 'date', 'created_at')
    search_fields = ('client__full_name',)
    list_filter = ('date', 'created_at')
    inlines = [SaleItemInline]
    autocomplete_fields = ['client']

# SalaryPayment Admin
@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('worker', 'amount', 'currency_type', 'date', 'created_at')
    search_fields = ('worker__full_name',)
    list_filter = ('currency_type', 'date', 'created_at')
    autocomplete_fields = ['worker', 'creator']