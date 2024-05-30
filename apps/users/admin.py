from django.contrib import admin


from apps.users.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'user_name', 'display_users', 'display_groups', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('email', 'user_name',)
    search_fields = ('email', 'user_name', 'display_users',)

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    display_groups.short_description = 'Группа'

    def display_users(self, obj):
        return f'{obj.first_name} {obj.last_name} {obj.middle_name}'
    display_users.short_description = 'ФИО'
