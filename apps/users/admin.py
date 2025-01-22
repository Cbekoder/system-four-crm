from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from apps.users.models import User

# unregister the default Group model
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
    )
    list_display_links = ("id", "username", "first_name", "last_name")
    search_fields = ("id", "username", "first_name", "last_name")
    list_filter = ("is_active",)
    ordering = ("-id",)