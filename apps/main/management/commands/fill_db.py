import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import connection

from apps.blog.models import Articles
from apps.clients.models import Clients
from apps.main.management.commands.create_su import Command as command_create_su
from apps.messages_.models import Messages
from apps.newsletters.models import Newsletters, Logs
from apps.users.models import Users
from config.settings import BASE_DIR

DICT_FIXTURES = {
    'permissions': {'file': '001_permissions_data'},
    'groups': {'file': '002_groups_data'},
    'users': {'file': '003_users_data'},
    'articles': {'file': '004_articles_data'},
    'clients': {'file': '005_clients_data'},
    'messages': {'file': '006_messages_data'},
    'newsletters': {'file': '007_newsletters_data'},
    'logs': {'file': '008_logs_data'},
}


class Command(BaseCommand):
    help = 'Кастомная команда для заполнения таблиц в БД'

    def add_arguments(self, parser):
        parser.add_argument(
            '--table', nargs='+', type=str, help='Specify which table(s) to fill'
        )

    @staticmethod
    def read_fixtures_json(filename: str) -> list:
        """Retrieve data from a fixture file in JSON format"""
        with open(f'{BASE_DIR}/fixtures/{filename}.json', encoding='UTF-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def fill_table_permissions():
        """Fill the Permissions table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE auth_permission RESTART IDENTITY CASCADE;")

        permissions_data = Command.read_fixtures_json(DICT_FIXTURES['permissions']['file'])
        permissions = []
        for permission in permissions_data:
            content_type_id = permission['fields']['content_type']
            content_type = ContentType.objects.get(id=content_type_id)
            permissions.append(
                Permission(
                    name=permission['fields']['name'],
                    content_type=content_type,
                    codename=permission['fields']['codename'],
                )
            )

        Permission.objects.bulk_create(permissions)

    @staticmethod
    def fill_table_groups():
        """Fill the Groups table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE auth_group RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE auth_group_permissions RESTART IDENTITY CASCADE;")

        groups_data = Command.read_fixtures_json(DICT_FIXTURES['groups']['file'])
        groups = []
        group_permissions = []

        for group in groups_data:
            group_instance = Group(name=group['fields']['name'])
            group_instance.save()
            groups.append(group_instance)

            permission_ids = group['fields']['permissions']
            group_permissions.append((group_instance, permission_ids))

        for group_instance, permission_ids in group_permissions:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group_instance.permissions.set(permissions)

    @staticmethod
    def fill_table_users():
        """Fill the Users table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE _us_users RESTART IDENTITY CASCADE;")

        users_data = Command.read_fixtures_json(DICT_FIXTURES['users']['file'])

        for user_data in users_data:
            user = Users.objects.create(
                password=make_password(user_data['fields']['password']),
                last_login=user_data['fields']['last_login'],
                is_superuser=user_data['fields']['is_superuser'],
                is_staff=user_data['fields']['is_staff'],
                is_active=user_data['fields']['is_active'],
                date_joined=user_data['fields']['date_joined'],
                email=user_data['fields']['email'],
                user_name=user_data['fields']['user_name'],
                first_name=user_data['fields']['first_name'],
                last_name=user_data['fields']['last_name'],
                middle_name=user_data['fields']['middle_name'],
                country=user_data['fields']['country'],
                city=user_data['fields']['city'],
                phone=user_data['fields']['phone'],
                birthday=user_data['fields']['birthday'],
                avatar=user_data['fields']['avatar'],
                token=user_data['fields']['token'],
            )

            # Связываем пользователя с группами
            group_ids = user_data['fields']['groups']
            user.groups.add(*group_ids)

    @staticmethod
    def fill_table_articles():
        """Fill the Articles table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE _bl_articles RESTART IDENTITY CASCADE;")

        articles_data = Command.read_fixtures_json(DICT_FIXTURES['articles']['file'])
        articles = [
            Articles(
                title=article['fields']['title'],
                slug=article['fields']['slug'],
                text=article['fields']['text'],
                img=article['fields']['img'],
                views=article['fields']['views'],
                created_at=article['fields']['created_at'],
                updated_at=article['fields']['updated_at'],
                is_published=article['fields']['is_published'],
                author_id=article['fields']['author']
            ) for article in articles_data
        ]

        Articles.objects.bulk_create(articles)

    @staticmethod
    def fill_table_clients():
        """Fill the Clients table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE _cl_clients RESTART IDENTITY CASCADE;")

        clients_data = Command.read_fixtures_json(DICT_FIXTURES['clients']['file'])

        for client in clients_data:
            owner_id = client['fields']['owner']
            owner_instance = Users.objects.get(pk=owner_id)

            client_instance = Clients(
                first_name=client['fields']['first_name'],
                last_name=client['fields']['last_name'],
                middle_name=client['fields']['middle_name'],
                email=client['fields']['email'],
                comment=client['fields']['comment'],
                birthday=client['fields']['birthday'],
                owner=owner_instance,
            )
            client_instance.save()

    @staticmethod
    def fill_table_messages():
        """Fill the Messages table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE _ms_messages RESTART IDENTITY CASCADE;")

        messages_data = Command.read_fixtures_json(DICT_FIXTURES['messages']['file'])

        for message in messages_data:
            owner_id = message['fields']['owner']
            owner_instance = Users.objects.get(pk=owner_id)
            message_instance = Messages(
                subject_letter=message['fields']['subject_letter'],
                text_letter=message['fields']['text_letter'],
                img_letter=message['fields']['img_letter'],
                owner=owner_instance,
            )
            message_instance.save()

    @staticmethod
    def fill_table_newsletters():
        """Fill the Newsletters table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE _ns_newsletters RESTART IDENTITY CASCADE;")
            cursor.execute("ALTER SEQUENCE _ns_newsletters_id_seq RESTART WITH 1;")

        newsletters_data = Command.read_fixtures_json(DICT_FIXTURES['newsletters']['file'])
        newsletters = []

        for newsletter in newsletters_data:
            owner_id = newsletter['fields']['owner']
            owner_instance = Users.objects.get(pk=owner_id) if owner_id else None

            message_id = newsletter['fields']['message']
            message_instance = Messages.objects.get(pk=message_id)

            newsletter_instance = Newsletters(
                name_newsletter=newsletter['fields']['name_newsletter'],
                date_first_mailing=newsletter['fields']['date_first_mailing'],
                frequency_mailing=newsletter['fields']['frequency_mailing'],
                date_next_mailing=newsletter['fields']['date_next_mailing'],
                state_mailing=newsletter['fields']['state_mailing'],
                message=message_instance,
                is_active=newsletter['fields']['is_active'],
                owner=owner_instance
            )
            newsletter_instance.save()

            # Add clients after saving the newsletter instance
            client_ids = newsletter['fields']['clients']
            clients = Clients.objects.filter(pk__in=client_ids)
            newsletter_instance.clients.set(clients)

            newsletter_instance.save()

    @staticmethod
    def fill_table_logs():
        """Fill the Logs table with data"""
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE _ns_logs RESTART IDENTITY CASCADE;")

        logs_data = Command.read_fixtures_json(DICT_FIXTURES['logs']['file'])

        for log in logs_data:
            newsletter_id = log['fields']['newsletter']
            newsletter_instance = Newsletters.objects.get(pk=newsletter_id)

            log_instance = Logs(
                newsletter=newsletter_instance,
                date_last_mailing=log['fields']['date_last_mailing'],
                status_mailing=log['fields']['status_mailing'],
                response_mail_server=log['fields']['response_mail_server']
            )
            log_instance.save()

    def handle(self, *args, **options):
        tables_to_fill = options['table']

        if not tables_to_fill:
            self.stdout.write(self.style.ERROR('Please specify at least one table to fill using --table option.'))
            return

        elif 'users' in tables_to_fill:
            self.stdout.write('Заполняем таблицы "permissions", "groups", "users"...')

            self.stdout.write('Заполняем таблицу "permissions"...')
            self.fill_table_permissions()
            self.stdout.write(self.style.SUCCESS('Таблица "permissions" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "groups"...')
            self.fill_table_groups()
            self.stdout.write(self.style.SUCCESS('Таблица "groups" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "users"...')
            self.fill_table_users()
            command_create_su.create_superuser()
            self.stdout.write(self.style.SUCCESS('Таблица "users" успешно заполнена...'))

        elif 'articles' in tables_to_fill:
            self.stdout.write('Заполняем таблицу "articles"...')
            self.fill_table_articles()
            self.stdout.write(self.style.SUCCESS('Таблица "articles" успешно заполнена...'))

        elif 'newsletters' in tables_to_fill:
            self.stdout.write('Заполняем таблицы "clients", "messages", "newsletters", "logs"...')

            self.stdout.write('Заполняем таблицу "clients"...')
            self.fill_table_clients()
            self.stdout.write(self.style.SUCCESS('Таблица "clients" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "messages"...')
            self.fill_table_messages()
            self.stdout.write(self.style.SUCCESS('Таблица "messages" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "newsletters"...')
            self.fill_table_newsletters()
            self.stdout.write(self.style.SUCCESS('Таблица "newsletters" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "logs"...')
            self.fill_table_logs()
            self.stdout.write(self.style.SUCCESS('Таблица "logs" успешно заполнена...'))

        elif 'all' in tables_to_fill:
            self.stdout.write('Заполняем все таблицы...')

            self.stdout.write('Заполняем таблицу "permissions"...')
            self.fill_table_permissions()
            self.stdout.write(self.style.SUCCESS('Таблица "permissions" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "groups"...')
            self.fill_table_groups()
            self.stdout.write(self.style.SUCCESS('Таблица "groups" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "users"...')
            self.fill_table_users()
            command_create_su.create_superuser()
            self.stdout.write('Создаём суперпользователя (admin)...')
            self.stdout.write(self.style.SUCCESS('Таблица "users" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "articles"...')
            self.fill_table_articles()
            self.stdout.write(self.style.SUCCESS('Таблица "articles" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "clients"...')
            self.fill_table_clients()
            self.stdout.write(self.style.SUCCESS('Таблица "clients" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "messages"...')
            self.fill_table_messages()
            self.stdout.write(self.style.SUCCESS('Таблица "messages" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "newsletters"...')
            self.fill_table_newsletters()
            self.stdout.write(self.style.SUCCESS('Таблица "newsletters" успешно заполнена...'))

            self.stdout.write('Заполняем таблицу "logs"...')
            self.fill_table_logs()
            self.stdout.write(self.style.SUCCESS('Таблица "logs" успешно заполнена...'))

# Dumpdata
# python -Xutf8  manage.py dumpdata auth.permission > .\fixtures\001_permissions_data.json --indent 4
# python -Xutf8  manage.py dumpdata auth.group > .\fixtures\002_groups_data.json --indent 4
# python -Xutf8  manage.py dumpdata users.Users > .\fixtures\003_users_data.json --indent 4
# python -Xutf8  manage.py dumpdata blog.Articles > .\fixtures\004_articles_data.json --indent 4
# python -Xutf8  manage.py dumpdata clients.Clients > .\fixtures\005_clients_data.json --indent 4
# python -Xutf8  manage.py dumpdata messages_.Messages > .\fixtures\006_messages_data.json --indent 4
# python -Xutf8  manage.py dumpdata newsletters.Newsletters > .\fixtures\007_newsletters_data.json --indent 4
# python -Xutf8  manage.py dumpdata newsletters.Logs > .\fixtures\008_logs_data.json --indent 4
