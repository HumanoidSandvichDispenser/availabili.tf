# Generated by Django 5.1.2 on 2024-10-26 00:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_playermasteravailability_unique_master_availability_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerinfo_team',
            name='playtime',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='playermasteravailability',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 26, 0, 32, 4, 805564, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerteamavailability',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 26, 0, 32, 13, 959511, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
