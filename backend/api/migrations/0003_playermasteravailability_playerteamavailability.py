# Generated by Django 5.1.2 on 2024-10-24 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_playerinfo_team_team_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerMasterAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('playerinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.playerinfo')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('playerinfo', 'start_time'), name='unique_master_availability')],
            },
        ),
        migrations.CreateModel(
            name='PlayerTeamAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('playerinfo_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.playerinfo_team')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('playerinfo_team', 'start_time'), name='unique_team_availability')],
            },
        ),
    ]
