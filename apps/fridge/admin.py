from django.contrib import admin
from .models import *

@admin.register(FridgeExpense)
class FridgeExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'refrigerator', 'amount', 'currency_type', 'created_at']
    list_display_links = ['id', 'refrigerator']

@admin.register(Refrigerator)
class RefrigeratorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year']
    list_display_links = ['id', 'name']

@admin.register(ElectricityBill)
class ElectricityBillAdmin(admin.ModelAdmin):
    list_display = ['id', 'refrigerator', 'amount', 'description', 'created_at']
    list_display_links = ['id', 'refrigerator']