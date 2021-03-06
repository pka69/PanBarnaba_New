# Generated by Django 3.1.3 on 2021-01-28 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20210125_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='negative_reaction',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='negatives', to='posts.post', verbose_name='pozytywne'),
        ),
        migrations.AddField(
            model_name='post',
            name='positive_reaction',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='positives', to='posts.post', verbose_name='pozytywne'),
        ),
        migrations.AlterField(
            model_name='post',
            name='related_post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='post nadrzędny'),
        ),
    ]
