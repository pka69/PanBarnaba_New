from django.core.management.base import BaseCommand
from ._menu import refresh_menu


class Command(BaseCommand):
    help = 'refresh menu'

    def handle(self, *args, **options):
        refresh_menu()
        self.stdout.write(self.style.SUCCESS("Succesfully refreshed menu"))
