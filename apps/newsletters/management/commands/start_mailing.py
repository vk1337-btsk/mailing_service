from django.core.management.base import BaseCommand
from apps.newsletters.services import start_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        start_mailing()
