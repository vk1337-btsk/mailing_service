# Generated by Django 5.0.4 on 2024-05-30 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_', '0004_remove_messages_img_letter'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='img_letter',
            field=models.ImageField(blank=True, null=True, upload_to='messages/message', verbose_name='Картинка письма'),
        ),
    ]
