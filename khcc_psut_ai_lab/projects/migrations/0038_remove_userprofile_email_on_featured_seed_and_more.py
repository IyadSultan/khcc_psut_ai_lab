# Generated by Django 5.1.3 on 2024-11-23 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0037_alter_userprofile_email_on_bookmark_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="email_on_featured_seed",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="email_on_gold_seed",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="email_on_team_comment",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="email_on_team_discussion",
        ),
    ]
