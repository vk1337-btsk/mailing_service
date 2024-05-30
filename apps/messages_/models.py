from django.db import models

from config import settings


NULLABLE = {'null': True, 'blank': True}


class Messages(models.Model):
    subject_letter = models.CharField(max_length=250, verbose_name='Тема письма')
    text_letter = models.TextField(verbose_name='Текст письма')
    img_letter = models.ImageField(upload_to='messages/message', **NULLABLE, verbose_name='Картинка письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.subject_letter}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['subject_letter']
        db_table = '_ms_messages'
        db_table_comment = "Письма"
        permissions = [
            ('view_all_messages', 'Can view all Письмо'),
        ]
