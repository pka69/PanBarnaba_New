from django.core.management.base import BaseCommand

from ._libraries import importLibraries


class Command(BaseCommand):
    help = 'import libraries'

    def handle(self, *args, **options):
        importLibraries()
        self.stdout.write(self.style.SUCCESS("Succesfully imported libraries"))
