# Generated by Django 3.2.2 on 2021-06-18 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_alter_submission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solves', to='challenges.challenge'),
        ),
    ]