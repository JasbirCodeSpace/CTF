# Generated by Django 3.2.2 on 2021-06-03 17:44

import challenges.models.challenge
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('decription', models.TextField()),
                ('difficulty', models.IntegerField(choices=[(1, 'EASY'), (2, 'MEDIUM'), (3, 'HARD')])),
                ('hint', models.TextField()),
                ('score', models.IntegerField()),
                ('file', models.FileField(blank=True, null=True, upload_to=challenges.models.challenge.get_upload_path)),
                ('flag', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('num_solves', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.category')),
            ],
            options={
                'verbose_name': 'Challenge',
                'verbose_name_plural': 'Challenges',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('correct', models.BooleanField(default=False)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
            options={
                'verbose_name': 'Submission',
                'verbose_name_plural': 'Submissions',
            },
        ),
    ]
