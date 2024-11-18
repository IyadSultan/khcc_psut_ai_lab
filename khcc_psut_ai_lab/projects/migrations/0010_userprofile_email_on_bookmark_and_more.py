# Generated by Django 5.1.3 on 2024-11-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0009_follow"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email_on_bookmark",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email_on_clap",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email_on_comment",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email_on_follow",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="twitter_username",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
