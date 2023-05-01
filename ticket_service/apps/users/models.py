from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ticket_service.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from users.constants import UserRoleType


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    email = models.EmailField(
        _("email address"), unique=True, blank=False, null=False, max_length=254
    )

    first_name = models.CharField(_("First Name"), max_length=100, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=100, blank=True)
    is_active = models.BooleanField(
        _("active"), default=False, help_text=_("Active user")
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("whether the user can log into this admin site."),
    )
    role = models.CharField(
        _("Role"),
        max_length=20,
        choices=UserRoleType.choices,
        default=UserRoleType.PERSONNEL,
    )

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.email}"

    objects = UserManager()

    class Meta:
        verbose_name_plural = "users"
        ordering = ["-created_at", "email"]
        indexes = [models.Index(fields=["email"])]

    @property
    def role_name(self):
        return self.role.name
