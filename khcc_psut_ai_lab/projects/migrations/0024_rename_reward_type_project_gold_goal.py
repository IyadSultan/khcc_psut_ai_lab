# Generated by Django 5.1.3 on 2024-11-19 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0023_project_deadline_project_is_completed_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="reward_type",
            new_name="gold_goal",
        ),
    ]
