# Generated by Django 3.2.5 on 2023-06-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0024_auto_20230626_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='image',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='image',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
