# Generated by Django 3.1.3 on 2021-02-14 10:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scoring', '0002_auto_20210213_1428'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Scoring',
            new_name='Score',
        ),
    ]
