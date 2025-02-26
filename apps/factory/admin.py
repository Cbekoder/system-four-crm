from django.contrib import admin
from .models import *

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'balance']
    list_display_links = ['id', 'full_name']

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','quantity', 'size', 'weight', 'price', 'per_worker_fee']
    list_display_links = ['id', 'name']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'basket__name', 'client__first_name','quantity', 'amount' ]
    list_display_links = ['id', 'basket__name', 'client__first_name']

@admin.register(DailyWork)
class DailyWorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'worker', 'basket', 'quantity', 'amount']
    list_display_links = ['id', 'worker', 'basket']