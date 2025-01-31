from django.contrib import admin
from .models import *


@admin.register(Refrigerator)
class RefrigeratorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year']
    list_display_links = ['id', 'name']
