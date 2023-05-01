from django.db import models
from django.utils.translation import gettext_lazy as _
from ticket_service.common.models import TimeStampedModel
from .managers import OrganizationManager, TransportationManager


class Transportation(TimeStampedModel):
    type = models.CharField(_("Name"), max_length=50, unique=True)
    is_active = models.BooleanField(_("Is Organization Active"), default=False)

    objects = TransportationManager()

    class Meta:
        verbose_name = "Transportation"
        verbose_name_plural = "Transportations"

    def __str__(self):
        return f"{self.id}-{self.type}-{self.is_active}"


class Organization(TimeStampedModel):
    transportation_types = models.ManyToManyField(
        Transportation,
        related_name="organizations",
        blank=False,
    )
    name = models.CharField(_("Name"), max_length=200, unique=True)
    address = models.CharField(_("Address"), max_length=255, blank=True)
    is_active = models.BooleanField(_("Is Organization Active"), default=False)

    objects = OrganizationManager()

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"{self.id}-{self.name}-{self.is_active}"
