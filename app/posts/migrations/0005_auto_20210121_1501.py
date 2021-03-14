# Generated by Django 3.1.3 on 2021-01-21 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20210120_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-p_date', '-p_time'], 'permissions': (('moderate', 'Can moderate posts'),)},
        ),
        migrations.AlterField(
            model_name='post',
            name='external_link',
            field=models.URLField(default='', max_length=350, verbose_name='link'),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.CharField(default='', max_length=350, verbose_name='obrazek'),
        ),
    ]
