from django.core.management.base import BaseCommand, CommandError
from accounts.stable_matching.matcher import Matcher


class Command(BaseCommand):
    help = 'This command will run stable matching algorithm on user accounts'

    def handle(self, *args, **options):
        matcher = Matcher()
        matcher.run()
