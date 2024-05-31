from datetime import timedelta

from django.utils.translation import gettext as _

from django.db import models
from apps.clients.models import Clients
from apps.messages_.models import Messages

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Newsletters(models.Model):

    class StateOfMailing(models.TextChoices):
        CREATED = 'C', _("Создана")
        LAUNCHED = 'L', _("Запущена")
        FINISHED = 'F', _("Завершена")

    class PeriodicityOfMailing(models.TextChoices):
        ONCE_DAY = 'D', _("Ежедневно")
        ONCE_WEEK = 'W', _("Еженедельно")
        ONCE_MONTH = 'M', _("Ежемесячно")
        ONCE_YEAR = 'Y', _("Ежегодно")

    name_newsletter = models.CharField(max_length=100, verbose_name='Название рассылки')
    date_first_mailing = models.DateTimeField(verbose_name='Дата и время первой рассылки')
    frequency_mailing = models.CharField(max_length=1, default=PeriodicityOfMailing.ONCE_DAY,
                                         choices=PeriodicityOfMailing, verbose_name='Периодичность рассылки')
    date_next_mailing = models.DateTimeField(**NULLABLE, verbose_name='Дата и время следующей рассылки')
    state_mailing = models.CharField(max_length=1, default=StateOfMailing.CREATED, choices=StateOfMailing,
                                     verbose_name='Состояние рассылки')
    clients = models.ManyToManyField(Clients, related_name='clients')
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, verbose_name='Сообщение')
    is_active = models.BooleanField(default=True, verbose_name='Статус рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.name_newsletter}'

    def save(self, *args, **kwargs):
        if not self.date_next_mailing:
            if self.frequency_mailing == self.PeriodicityOfMailing.ONCE_DAY:
                self.date_next_mailing = self.date_first_mailing + timedelta(days=1)
            elif self.frequency_mailing == self.PeriodicityOfMailing.ONCE_WEEK:
                self.date_next_mailing = self.date_first_mailing + timedelta(days=7)
            elif self.frequency_mailing == self.PeriodicityOfMailing.ONCE_MONTH:
                self.date_next_mailing = self.date_first_mailing + timedelta(days=30)
            else:
                self.date_next_mailing = self.date_first_mailing + timedelta(days=365)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['date_first_mailing', 'name_newsletter']
        db_table = '_ns_newsletters'
        db_table_comment = "Рассылки"
        permissions = [
            ('set_newsletters_deactivate', 'Can deacticate Рассылка'),
            ('view_all_newsletters', 'Can view all Рассылка'),
        ]


class Logs(models.Model):

    class StatusOfLogs(models.TextChoices):
        SUCCESS = "Успешно", _("Успешно")
        FAILED = "Безуспешно", _("Безуспешно")
        PARTIALLY = "Частично успешно", _("Частично успешно")

    newsletter = models.ForeignKey(Newsletters, on_delete=models.CASCADE, related_name='logs')
    date_last_mailing = models.DateTimeField(verbose_name='Дата последней попытки')
    status_mailing = models.CharField(choices=StatusOfLogs, verbose_name='Статус рассылки')
    response_mail_server = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f'{self.newsletter} {self.status_mailing}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['newsletter', 'date_last_mailing']
        db_table = '_ns_logs'
        db_table_comment = "Попытки рассылки"
