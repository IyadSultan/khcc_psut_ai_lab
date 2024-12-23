# Generated by Django 5.1.3 on 2024-11-18 04:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0007_rename_clapped_at_clap_created_at_bookmark_notes_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("comment", "Comment"),
                    ("follow", "Follow"),
                    ("clap", "Clap"),
                    ("bookmark", "Bookmark"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="sender",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
