# Generated by Django 3.2.5 on 2023-06-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0005_auto_20230606_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspireuser',
            name='pwcodecreated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]