# Generated by Django 4.0.2 on 2022-02-15 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_profile_csv"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="firstName",
            field=models.CharField(default="", max_length=25),
        ),
        migrations.AddField(
            model_name="profile",
            name="lastName",
            field=models.CharField(default="", max_length=25),
        ),
    ]