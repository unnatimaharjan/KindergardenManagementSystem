# Generated by Django 4.2.2 on 2024-02-17 10:31

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Teacher",
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
                ("user_id", models.IntegerField(max_length=3)),
                ("subject", models.CharField(max_length=255)),
                ("_class", models.CharField(max_length=255)),
            ],
        ),
    ]