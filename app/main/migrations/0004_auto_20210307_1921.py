# Generated by Django 3.1.3 on 2021-03-07 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210307_1919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['group', 'sequence', 'id']},
        ),
        migrations.AddField(
            model_name='menu',
            name='sequence',
            field=models.IntegerField(default=0),
        ),
    ]
