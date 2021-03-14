from django.core.management.base import BaseCommand

from ._pricecheck import loadBookPrices


class Command(BaseCommand):
    help = 'read prices from lubimyczytac.pl'

    def handle(self, *args, **options):
        counter = loadBookPrices()
        if not counter:
            self.stdout.write(self.style.ERROR("Failed updated prices from lubimyczytac.pl"))
            return
        self.stdout.write(self.style.SUCCESS("Succesfully updatet {} prices from lubimyczytac.pl".format(counter)))
