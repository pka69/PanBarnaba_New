from django.core.management.base import BaseCommand
from ._menu import create_menu


class Command(BaseCommand):
    help = 'create menu'

    def handle(self, *args, **options):
        create_menu()
        self.stdout.write(self.style.SUCCESS("Succesfully created menu"))
