# Generated by Django 3.2.2 on 2021-09-18 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210821_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='college',
            field=models.CharField(default='NITT', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='year',
            field=models.IntegerField(choices=[(1, 'First Year'), (2, 'Second Year'), (3, 'Third Year')], default=2),
            preserve_default=False,
        ),
    ]