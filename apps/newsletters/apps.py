from time import sleep
from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.newsletters'

    # def ready(self):
    #     from apps.newsletters.management.commands.runapscheduler import Command as RunApScheduler
    #     sleep(2)
    #     RunApScheduler.handle(self)
