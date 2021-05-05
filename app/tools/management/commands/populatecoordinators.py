from django.core.management.base import BaseCommand

from ._libraries import importCoordinators


class Command(BaseCommand):
    help = 'import DKK coordinators '

    def handle(self, *args, **options):
        importCoordinators()
        self.stdout.write(self.style.SUCCESS("Succesfully imported DKK coordinators"))
