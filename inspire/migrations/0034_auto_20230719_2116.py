# Generated by Django 3.2.5 on 2023-07-19 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0033_auto_20230719_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favourite',
            name='likes',
        ),
        migrations.AddField(
            model_name='text',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
