# Generated by Django 3.1.3 on 2021-01-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Sudoku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.TextField(db_index=True)),
                ('level', models.CharField(max_length=20)),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('border', models.CharField(max_length=5)),
                ('fix', models.BooleanField()),
                ('blocks', models.ManyToManyField(related_name='cells', to='sudoku.Block')),
                ('sudoku', models.ManyToManyField(related_name='cells', to='sudoku.Sudoku')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='sudoku',
            field=models.ManyToManyField(related_name='blocks', to='sudoku.Sudoku'),
        ),
    ]
