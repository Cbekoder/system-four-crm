from django.contrib import admin
from .models import *


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id','section', 'amount', 'currency_type', 'created_at']
    list_display_links = ['id','section', 'amount']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id','section', 'amount', 'currency_type', 'created_at']
    list_display_links = ['id', 'section','amount']