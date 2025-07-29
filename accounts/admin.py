from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AppUser


# Register your models here.
@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            ("Permissions",),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates",), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ('email', 'is_active', 'is_staff',)
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
