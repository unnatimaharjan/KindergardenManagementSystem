# Generated by Django 4.2.2 on 2024-02-26 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kmsd", "0004_attendance_grade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="grade",
            field=models.FloatField(default=0.0),
        ),
    ]