# projects/models/analytics.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PageVisit(models.Model):
    path = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['path', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

class EventTracker(models.Model):
    EVENT_TYPES = [
        ('view', 'Page View'),
        ('click', 'Click'),
        ('scroll', 'Scroll'),
        ('clap', 'Clap'),
        ('comment', 'Comment'),
        ('bookmark', 'Bookmark'),
    ]

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    target = models.CharField(max_length=100, blank=True)  # e.g., button id, element class
    metadata = models.JSONField(default=dict, blank=True)  # Additional event data

    class Meta:
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]