# Generated by Django 3.2.5 on 2023-06-23 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0021_notification_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
