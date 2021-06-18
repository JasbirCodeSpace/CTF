# Generated by Django 3.2.2 on 2021-06-18 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_team'),
        ('challenges', '0003_alter_submission_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='accounts.profile'),
        ),
    ]
