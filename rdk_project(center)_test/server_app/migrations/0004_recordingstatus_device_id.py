# Generated by Django 5.1.2 on 2024-11-14 03:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server_app", "0003_recordingstatus_start_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordingstatus",
            name="device_id",
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
