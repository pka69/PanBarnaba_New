from django.core.management.base import BaseCommand

from tools.mail import moderatorInform



class Command(BaseCommand):
    help = 'send email to moderators if neccessary'
    def handle(self, *args, **options):
        counter = moderatorInform()
        if not counter:
            self.stdout.write(self.style.SUCCESS("Nie ma nic do wysłania"))
            return
        self.stdout.write(self.style.SUCCESS("Mail został wysłany do moderatorów"))
