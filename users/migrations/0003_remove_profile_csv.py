# Generated by Django 4.0.2 on 2022-02-15 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile_csv"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="csv",
        ),
    ]
