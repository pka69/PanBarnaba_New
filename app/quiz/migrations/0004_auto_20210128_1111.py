# Generated by Django 3.1.3 on 2021-01-28 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['qlevel', 'qgroup']},
        ),
    ]
