# Generated by Django 3.2.5 on 2023-06-24 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0022_auto_20230623_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='readablecreated',
            field=models.CharField(default='Nov 19', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='readablecreated',
            field=models.CharField(default='Nov 19', max_length=50),
            preserve_default=False,
        ),
    ]