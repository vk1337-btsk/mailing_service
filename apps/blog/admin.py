from django.contrib import admin

from apps.blog.models import Articles


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'slug', 'views', 'is_published', 'created_at', 'updated_at')
    list_filter = ('title', 'author')
    search_fields = ('title', 'author')
