# Generated by Django 4.0.3 on 2022-03-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegramBot', '0006_schedule_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule_messages',
            name='type',
            field=models.CharField(default='text', max_length=100),
        ),
    ]