from django.core.management.base import BaseCommand

from ._exportcontent import importContent


class Command(BaseCommand):
    help = 'posts export'

    def handle(self, *args, **options):
        # counter = changeHTML()
        counter = importContent()
        self.stdout.write(self.style.SUCCESS("Succesfully imported {} content posts".format(counter)))