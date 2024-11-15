# Generated by Django 5.1.2 on 2024-11-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server_app", "0006_recordingsession"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recording",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("total_time", models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name="RecordingSession",
        ),
    ]
