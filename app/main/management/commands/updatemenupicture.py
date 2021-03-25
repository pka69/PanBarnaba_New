from django.core.management.base import BaseCommand
from ._menu import update_menu_picture


class Command(BaseCommand):
    help = 'update menu picture'

    def handle(self, *args, **options):
        update_menu_picture()
        self.stdout.write(self.style.SUCCESS("Succesfully updated menu picture"))
