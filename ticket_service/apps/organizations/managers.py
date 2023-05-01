from django.db import models

class OrganizationManager(models.Manager):
    def get_active_or_none(self, *args, **kwargs):
        try:
            return super(TransportationManager, self).get(is_active=True, **kwargs)
        except :
            return None

class TransportationManager(models.Manager):
    def get_active_or_none(self, *args, **kwargs):
        try:
            return super(TransportationManager, self).get(is_active=True, **kwargs)
        except :
            return None
