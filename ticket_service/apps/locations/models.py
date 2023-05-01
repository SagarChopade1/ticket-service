from django.db import models
from django.utils.translation import gettext_lazy as _
from ticket_service.common.models import TimeStampedModel
from users.models import User

class Location(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT, related_name="locations",null=True,blank=True)
    is_active = models.BooleanField(_("Is Location Active"), default=False)


    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.id}-{self.name}-{self.is_active}"