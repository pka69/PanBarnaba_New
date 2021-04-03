from django.core.management.base import BaseCommand
from ._postmanagement import delRejected


class Command(BaseCommand):
    help = 'delete rejected posts'

    def handle(self, *args, **options):
        delRejected()
        self.stdout.write(self.style.SUCCESS("Succesfully deleted rejected posts"))