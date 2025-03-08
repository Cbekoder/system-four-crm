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


@admin.register(SaleItem)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'basket__name', 'sale__client__first_name','quantity' ]
    list_display_links = ['id', 'basket__name', 'sale__client__first_name']

class UserBasketCountInline(admin.TabularInline):
    model = UserBasketCount
    extra = 1
    fields = ('basket', 'quantity')
    readonly_fields = ()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "basket":
            kwargs["queryset"] = Basket.objects.all().order_by('id')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(UserDailyWork)
class UserDailyWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker_name', 'amount', 'created_at', 'description_short')
    list_filter = ('worker', 'created_at')
    search_fields = ('worker__full_name', 'description')
    ordering = ('-created_at',)
    fields = ('worker', 'amount', 'description', 'created_at')
    inlines = [UserBasketCountInline]

    def worker_name(self, obj):
        return obj.worker.full_name
    worker_name.short_description = "Ishchi"

    def description_short(self, obj):
        return obj.description[:50] + '...' if obj.description and len(obj.description) > 50 else obj.description
    description_short.short_description = "Tavsif"

    readonly_fields = ('created_at',)