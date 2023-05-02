
from django.db import models
from django.utils.translation import gettext_lazy as _
from ticket_service.common.models import TimeStampedModel
from users.models import User
from organizations.models import Transportation
from locations.models import Location
from tickets.constants import CurrencyType

class Ticket(TimeStampedModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_tickets')
    transportation_type = models.ForeignKey(Transportation, on_delete=models.CASCADE,related_name="transportation_tickets")
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passenger_tickets',null=True,blank=True)
    passenger_name = models.CharField(max_length=255,blank=False, null=False,default="")
    source = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='source_tickets')
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destination_tickets')
    seat_number = models.CharField(max_length=10,blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=False, null=False)
    currency_type = models.CharField(
        _("Currency"),
        max_length=20,
        choices=CurrencyType.choices,
        default=CurrencyType.USD,
    )
    journey_start_time = models.DateTimeField(blank=False, null=False)
    journey_end_time = models.DateTimeField(blank=False, null=False)
    qr_code = models.BinaryField(blank=False, null=False)
    is_qr_code_valid = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id}|{self.source}|{self.destination}|{self.is_cancelled}"


    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-created_at"]
