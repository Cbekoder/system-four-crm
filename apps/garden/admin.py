from django.contrib import admin
from .models import *


@admin.register(Gardener)
class GardenerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'balance']
    list_display_links = ['id', 'full_name']

@admin.register(GardenSalaryPayment)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'gardener', 'amount', 'currency_type']
    list_display_links = ['id', 'gardener']

