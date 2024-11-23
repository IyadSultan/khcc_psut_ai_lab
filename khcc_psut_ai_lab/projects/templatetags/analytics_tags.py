# projects/templatetags/analytics_tags.py

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('analytics/google_analytics.html')
def google_analytics():
    """
    Renders Google Analytics tracking code if GOOGLE_ANALYTICS_ID is set
    """
    return {
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'debug': settings.DEBUG
    }