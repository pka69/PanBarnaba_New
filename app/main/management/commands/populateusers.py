from django.core.management.base import BaseCommand

from ._users import create_users


class Command(BaseCommand):
    help = 'create users'

    def handle(self, *args, **options):
        create_users()
        self.stdout.write(self.style.SUCCESS("Succesfully created users"))
