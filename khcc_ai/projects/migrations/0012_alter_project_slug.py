# Generated by Django 5.1.3 on 2024-11-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0011_alter_project_github_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
