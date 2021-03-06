# Generated by Django 3.1.3 on 2021-01-20 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.IntegerField(choices=[(0, 'News'), (1, 'Quotation'), (2, 'Forum'), (3, 'Notes'), (4, 'Post'), (5, 'BookPrice')], db_index=True, verbose_name='grupa')),
                ('subgroup', models.IntegerField(choices=[(0, 'News'), (1, 'Quotation'), (2, 'Forum'), (3, 'Notes'), (4, 'Post'), (5, 'BookPrice')], default='', verbose_name='podgrupa')),
                ('p_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='data')),
                ('p_time', models.TimeField(auto_now_add=True, db_index=True, verbose_name='godzina')),
                ('stage', models.IntegerField(choices=[(0, 'posted'), (1, 'approved'), (-1, 'rejected')], db_index=True, default=0, verbose_name='status')),
                ('content', models.TextField(default='', verbose_name='treść')),
                ('dec_content', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='wartość')),
                ('external_link', models.URLField(default='', verbose_name='link')),
                ('picture', models.CharField(max_length=128, verbose_name='obrazek')),
                ('moderator', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='set_moderation', to=settings.AUTH_USER_MODEL, verbose_name='moderator')),
                ('owner', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='set_posts', to=settings.AUTH_USER_MODEL, verbose_name='właściciel')),
                ('related_post', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='post nadrzędny')),
            ],
            options={
                'ordering': ['-p_date', '-p_time'],
            },
        ),
    ]
