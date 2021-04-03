from django.core.management.base import BaseCommand
from ._menu import new_compare


class Command(BaseCommand):
    help = 'create menu new position - Differences'

    def handle(self, *args, **options):
        new_compare()
        self.stdout.write(self.style.SUCCESS("Succesfully created new menu position"))
