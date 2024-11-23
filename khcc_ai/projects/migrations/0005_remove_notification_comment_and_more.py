# Generated by Django 5.1.3 on 2024-11-17 23:06

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_notification"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="comment",
        ),
        migrations.AlterField(
            model_name="notification",
            name="notification_type",
            field=models.CharField(
                choices=[
                    ("clap", "Clap"),
                    ("comment", "Comment"),
                    ("reply", "Reply"),
                    ("mention", "Mention"),
                    ("follow", "Follow"),
                    ("rating", "Rating"),
                    ("bookmark", "Bookmark"),
                ],
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="ProjectAnalytics",
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
                ("view_count", models.PositiveIntegerField(default=0)),
                ("unique_visitors", models.PositiveIntegerField(default=0)),
                ("github_clicks", models.PositiveIntegerField(default=0)),
                ("avg_time_spent", models.DurationField(default=datetime.timedelta)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                ("direct_traffic", models.PositiveIntegerField(default=0)),
                ("social_traffic", models.PositiveIntegerField(default=0)),
                ("search_traffic", models.PositiveIntegerField(default=0)),
                ("referral_traffic", models.PositiveIntegerField(default=0)),
                ("desktop_visits", models.PositiveIntegerField(default=0)),
                ("mobile_visits", models.PositiveIntegerField(default=0)),
                ("tablet_visits", models.PositiveIntegerField(default=0)),
                ("chrome_visits", models.PositiveIntegerField(default=0)),
                ("firefox_visits", models.PositiveIntegerField(default=0)),
                ("safari_visits", models.PositiveIntegerField(default=0)),
                ("edge_visits", models.PositiveIntegerField(default=0)),
                ("other_browsers", models.PositiveIntegerField(default=0)),
                ("unique_visitors_weekly", models.PositiveIntegerField(default=0)),
                ("unique_visitors_monthly", models.PositiveIntegerField(default=0)),
                ("github_clicks_weekly", models.PositiveIntegerField(default=0)),
                ("github_clicks_monthly", models.PositiveIntegerField(default=0)),
                (
                    "project",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analytics",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Project analytics",
            },
        ),
        migrations.CreateModel(
            name="Bookmark",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "notes",
                    models.TextField(
                        blank=True, help_text="Add private notes about this project"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmarks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "project")},
            },
        ),
        migrations.CreateModel(
            name="Rating",
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
                (
                    "score",
                    models.IntegerField(
                        choices=[
                            (1, "1 - Poor"),
                            (2, "2 - Fair"),
                            (3, "3 - Good"),
                            (4, "4 - Very Good"),
                            (5, "5 - Excellent"),
                        ]
                    ),
                ),
                ("review", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "user")},
            },
        ),
    ]