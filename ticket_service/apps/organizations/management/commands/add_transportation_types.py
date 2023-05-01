from django.core.management.base import BaseCommand, CommandError
from organizations.models import Transportation
from django.db import transaction
from django.conf import settings
import csv
import os.path


class Command(BaseCommand):
    help = "Add Transportation types in the database."

    @transaction.atomic
    def handle(self, *args, **options):
        file = os.path.join(
            settings.BASE_DIR,
            "apps",
            "organizations",
            "migrations",
            "seeds",
            "transportation_types.csv",
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
        Transportation.objects.create(type=row["type"], is_active=row["is_active"])
