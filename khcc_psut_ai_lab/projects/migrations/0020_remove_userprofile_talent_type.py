# Generated by Django 5.1.3 on 2024-11-19 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0019_userprofile_talent_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="talent_type",
        ),
    ]
