# Generated by Django 5.0.4 on 2024-05-31 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('comment', models.TextField(blank=True, max_length=200, null=True, verbose_name='Комментарий')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'db_table': '_cl_clients',
                'db_table_comment': 'Клиенты',
                'ordering': ['first_name', 'last_name', 'middle_name'],
                'permissions': [('view_all_clients', 'Can view all Клиент')],
            },
        ),
    ]