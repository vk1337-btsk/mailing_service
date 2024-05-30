from django.contrib import admin

from apps.newsletters.models import Newsletters, Logs
from apps.messages_.models import Messages


@admin.register(Newsletters)
class NewslettersAdmin(admin.ModelAdmin):
    list_display = ('name_newsletter', 'date_first_mailing', 'frequency_mailing', 'state_mailing', 'is_active')
    list_filter = ('name_newsletter',)
    search_fields = ('name_newsletter',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'date_last_mailing', 'status_mailing',)
    list_filter = ('newsletter',)
    search_fields = ('newsletter',)


@admin.register(Messages)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject_letter',)
    list_filter = ('subject_letter',)
    search_fields = ('subject_letter',)
