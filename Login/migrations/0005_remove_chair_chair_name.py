# Generated by Django 3.1.1 on 2020-10-22 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0004_auto_20201020_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chair',
            name='chair_name',
        ),
    ]
