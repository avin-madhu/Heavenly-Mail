# Generated by Django 5.1.1 on 2024-09-21 15:27

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledemail',
            name='last_active',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='scheduledemail',
            name='send_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='scheduledemail',
            name='time_limit',
            field=models.DurationField(default=datetime.timedelta(days=365)),
        ),
    ]