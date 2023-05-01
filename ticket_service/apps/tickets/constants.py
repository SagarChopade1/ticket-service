from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices


class CurrencyType(TextChoices):
    USD= 'USD', 'US Dollar'
