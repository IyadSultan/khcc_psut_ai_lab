# Generated by Django 5.1.3 on 2024-11-19 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0020_remove_userprofile_talent_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="talent_type",
            field=models.CharField(
                choices=[
                    ("ai", "AI Talent"),
                    ("healthcare", "Healthcare Talent"),
                    ("quality", "Quality Talent"),
                    ("engineering", "Engineering Talent"),
                    ("planner", "Planner Talent"),
                    ("design", "Design Talent"),
                    ("lab", "Lab Talent"),
                ],
                default="ai",
                max_length=20,
                verbose_name="Talent Type",
            ),
        ),
    ]
