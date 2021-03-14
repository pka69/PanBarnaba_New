from django.core.management.base import BaseCommand

from ._sudoku import createSudoku


class Command(BaseCommand):
    help = 'create Sudoku models'

    def handle(self, *args, **options):
        createSudoku()
        self.stdout.write(self.style.SUCCESS("Succesfully created Sudoku models"))
