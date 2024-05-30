from django.contrib import admin

from apps.clients.models import Clients


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'email', 'birthday',)
    list_filter = ('first_name', 'last_name', 'middle_name', 'email', 'birthday',)
    search_fields = ('first_name', 'last_name', 'middle_name',)