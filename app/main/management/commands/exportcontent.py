from django.core.management.base import BaseCommand

from ._exportcontent import exportContent


class Command(BaseCommand):
    help = 'posts export'

    def handle(self, *args, **options):
        # counter = changeHTML()
        counter = exportContent()
        self.stdout.write(self.style.SUCCESS("Succesfully exported {} content posts".format(counter)))
