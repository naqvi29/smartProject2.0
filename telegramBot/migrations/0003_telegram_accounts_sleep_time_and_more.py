# Generated by Django 4.0.1 on 2022-03-08 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegramBot', '0002_telegram_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegram_accounts',
            name='sleep_time',
            field=models.CharField(default=2, max_length=120),
        ),
        migrations.AddField(
            model_name='telegram_accounts',
            name='sleep_time_first',
            field=models.CharField(default=2, max_length=120),
        ),
    ]
