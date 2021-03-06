# Generated by Django 4.0.2 on 2022-02-15 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0003_remove_profile_csv"),
    ]

    operations = [
        migrations.CreateModel(
            name="CSVFiles",
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
                ("name", models.CharField(max_length=50)),
                (
                    "csv",
                    models.FileField(
                        default="default.csv", upload_to="spotify_csv"
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.profile",
                    ),
                ),
            ],
        ),
    ]
