# Generated by Django 3.2.5 on 2023-07-17 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0030_video_tn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='tn',
        ),
    ]