# Generated by Django 4.0.1 on 2022-03-08 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegramBot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Telegram_Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=100)),
                ('account_id', models.CharField(max_length=100)),
                ('answers', models.TextField()),
            ],
        ),
    ]
