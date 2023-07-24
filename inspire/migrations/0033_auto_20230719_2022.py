# Generated by Django 3.2.5 on 2023-07-19 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0032_auto_20230719_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='text',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='video',
            name='likes',
        ),
        migrations.AddField(
            model_name='favourite',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]