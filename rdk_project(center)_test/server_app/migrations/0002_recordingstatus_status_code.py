# Generated by Django 5.1.2 on 2024-11-13 06:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("server_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recordingstatus",
            name="status_code",
            field=models.IntegerField(default=0),
        ),
    ]
