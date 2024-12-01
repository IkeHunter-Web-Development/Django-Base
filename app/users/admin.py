"""
Users admin config.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


class UserAdmin(BaseUserAdmin):
    """Manager users in admin dashbaord."""

    readonly_fields = BaseUserAdmin.readonly_fields + ("date_joined", "date_modified")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
