# Generated by Django 3.1.3 on 2021-01-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0004_auto_20210116_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
