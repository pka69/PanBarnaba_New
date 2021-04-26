from django.core.management.base import BaseCommand
from ._menu import update_menu_links


class Command(BaseCommand):
    help = 'update menu links'

    def handle(self, *args, **options):
        update_menu_links()
        self.stdout.write(self.style.SUCCESS("Succesfully updated menu links"))
