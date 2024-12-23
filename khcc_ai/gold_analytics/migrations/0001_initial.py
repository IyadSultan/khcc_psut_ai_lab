# Generated by Django 5.1.3 on 2024-11-22 05:49

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PageMetrics",
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
                ("path", models.CharField(max_length=255, unique=True)),
                ("total_visits", models.PositiveIntegerField(default=0)),
                ("unique_visitors", models.PositiveIntegerField(default=0)),
                ("avg_time_spent", models.DurationField(default=datetime.timedelta)),
                ("bounce_rate", models.FloatField(default=0.0)),
                ("last_updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Page metrics",
            },
        ),
        migrations.CreateModel(
            name="VisitorSession",
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
                ("session_key", models.CharField(max_length=40, unique=True)),
                ("ip_address", models.GenericIPAddressField()),
                ("user_agent", models.TextField()),
                ("device_type", models.CharField(max_length=20)),
                ("browser", models.CharField(max_length=50)),
                ("os", models.CharField(max_length=50)),
                ("start_time", models.DateTimeField(auto_now_add=True)),
                ("end_time", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-start_time"],
            },
        ),
        migrations.CreateModel(
            name="PageVisit",
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
                ("session_key", models.CharField(max_length=40)),
                ("ip_address", models.GenericIPAddressField()),
                ("user_agent", models.TextField()),
                ("path", models.CharField(max_length=255)),
                ("referer", models.URLField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("time_spent", models.DurationField(blank=True, null=True)),
                ("object_id", models.PositiveIntegerField(null=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-timestamp"],
                "indexes": [
                    models.Index(
                        fields=["session_key"], name="gold_analyt_session_6cd5e7_idx"
                    ),
                    models.Index(fields=["path"], name="gold_analyt_path_8bfd5b_idx"),
                    models.Index(
                        fields=["timestamp"], name="gold_analyt_timesta_4a6e97_idx"
                    ),
                ],
            },
        ),
    ]
