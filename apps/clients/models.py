from django.db import models

from apps.blog.models import NULLABLE
from config import settings


class Clients(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    email = models.EmailField(max_length=100, verbose_name='Email')
    comment = models.TextField(max_length=200, **NULLABLE, verbose_name="Комментарий")
    birthday = models.DateField(**NULLABLE, verbose_name='День рождения')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='owner',
                              **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['first_name', 'last_name', 'middle_name']
        unique_together = ['email', 'owner']
        db_table = '_cl_clients'
        db_table_comment = "Клиенты"
        permissions = [
            ('view_all_clients', 'Can view all Клиент'),
        ]
