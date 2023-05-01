from django.core.management.base import BaseCommand, CommandError
from organizations.models import Organization,Transportation
from django.db import transaction
from django.conf import settings
import csv
import os.path


class Command(BaseCommand):
    help = "Add Organization types in the database."

    @transaction.atomic
    def handle(self, *args, **options):
        file = os.path.join(
            settings.BASE_DIR,
            "apps",
            "organizations",
            "migrations",
            "seeds",
            "organizations.csv",
        )
        if not file or not os.path.isfile(file):
            raise CommandError("File doesn't exist")

        try:
            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                for r_index, row in enumerate(reader):
                    self.__create_module_permission(row)
        except Exception as e:
            raise CommandError(str(e))
        self.stdout.write(self.style.SUCCESS("Successfully imported"))

    def __create_module_permission(self, row):
        org=Organization.objects.create(name=row["name"], address=row["address"],is_active=row["is_active"])
        org.transportation_types.add(Transportation.objects.get(type=row["transportation_types"]))