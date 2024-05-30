import configparser
import os

from django.core.management import BaseCommand

from apps.users.models import Users
from config.settings import BASE_DIR

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, "config.ini"), encoding='utf-8')


class Command(BaseCommand):

    @staticmethod
    def create_superuser():
        user = Users.objects.create(
            email=config['data_admin']['ADMIN_EMAIL'],
            user_name=config['data_admin']['ADMIN_USER_NAME'],
            first_name=config['data_admin']['ADMIN_FIRST_NAME'],
            last_name=config['data_admin']['ADMIN_LAST_NAME'],
            middle_name=config['data_admin']['ADMIN_MIDDLE_NAME'],
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password(config['data_admin']['ADMIN_PASSWORD'])
        user.save()

    def handle(self, *args, **options):
        self.create_superuser()
