# Generated by Django 3.1.3 on 2021-02-08 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20210129_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='qtype',
            field=models.IntegerField(choices=[(0, 'single'), (1, 'multi')]),
        ),
    ]