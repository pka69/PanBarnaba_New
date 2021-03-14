# Generated by Django 3.1.3 on 2021-03-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20210208_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.IntegerField(choices=[(0, 'News'), (1, 'Quotation'), (2, 'Forum'), (3, 'Notes'), (4, 'Post'), (5, 'BookPrice'), (6, 'Content'), (7, 'Message'), (8, 'Welcome')], db_index=True, verbose_name='grupa'),
        ),
    ]
