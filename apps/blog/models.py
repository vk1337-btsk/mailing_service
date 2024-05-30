from django.db import models
from pytils.translit import slugify

from config import settings


NULLABLE = {'null': True, 'blank': True}


class Articles(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название статьи")
    slug = models.CharField(max_length=100, null=True, blank=True, verbose_name="Slug статьи")
    text = models.TextField(verbose_name="Текст статьи")
    img = models.ImageField(upload_to='blog/news/', null=True, blank=True, verbose_name='Превью статьи',
                            default='blog/news/default.jpeg')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(default=False, verbose_name="Статус публикации")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                               verbose_name='Пользователь')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            queryset = Articles.objects.filter(slug=self.slug).exclude(pk=self.pk)
            counter = 1
            while queryset.exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
                queryset = Articles.objects.filter(slug=self.slug).exclude(pk=self.pk)
        super().save(args, kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
        db_table = '_bl_articles'
        db_table_comment = "Статьи"
