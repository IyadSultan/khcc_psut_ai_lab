from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class PageVisit(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    path = models.CharField(max_length=255)
    referer = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    time_spent = models.DurationField(null=True, blank=True)
    
    # For tracking specific object visits (e.g., projects, teams)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['path']),
            models.Index(fields=['timestamp']),
        ]

class VisitorSession(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=20)  # mobile, tablet, desktop
    browser = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-start_time']

class PageMetrics(models.Model):
    path = models.CharField(max_length=255, unique=True)
    total_visits = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    avg_time_spent = models.DurationField(default=timezone.timedelta)
    bounce_rate = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Page metrics" 