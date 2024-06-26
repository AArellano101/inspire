# Generated by Django 3.2.5 on 2023-07-22 05:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0034_auto_20230719_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='subcategories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), default=list, size=None),
        ),
        migrations.AddField(
            model_name='video',
            name='subcategories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), default=list, size=None),
        ),
    ]
