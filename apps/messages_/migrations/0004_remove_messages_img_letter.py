# Generated by Django 5.0.4 on 2024-05-30 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messages_', '0003_alter_messages_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='img_letter',
        ),
    ]
