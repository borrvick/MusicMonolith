# Generated by Django 4.0.2 on 2022-02-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="csv",
            field=models.FileField(
                default="default.csv", upload_to="spotify_csv"
            ),
        ),
    ]