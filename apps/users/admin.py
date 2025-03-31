from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User

# unregister the default Group model
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha maydonlar", {'fields': ('role', 'section', 'balance')}),
    )
    list_display = ('username', 'role', 'section', 'is_staff', 'is_active')
    list_filter = ('role', 'section', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ("-id",)