# Generated by Django 3.2.5 on 2023-06-14 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0009_alter_inspireuser_favourites'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspireuser',
            name='rememberme',
            field=models.BooleanField(default=False),
        ),
    ]
