import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from apps.newsletters.services import start_mailing

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Эта команда запускает процесс отправки рассылок на электронные почты клиентов. Перезапуск процесса каждые 10 секунд.
    """

    def handle(self, *args, **options):
        print('Инициализация планировщика..')
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            start_mailing,
            trigger=CronTrigger(second="*/10"),  # Every 30 seconds
            id="start_mailing",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Старт планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно остановлен!")
