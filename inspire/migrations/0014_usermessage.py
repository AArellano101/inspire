# Generated by Django 3.2.5 on 2023-06-15 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspire', '0013_auto_20230614_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, null=True)),
                ('email', models.CharField(max_length=70, null=True)),
                ('message', models.TextField(max_length=1000)),
            ],
        ),
    ]
