from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models import User


class UserAdmin(UserAdmin):
    readonly_fields = ("updated_at", "created_at")

    fieldsets = (
        (None, {"fields": ()}),
        (
            _("Personal info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name", "updated_at")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


admin.site.register(User, UserAdmin)
