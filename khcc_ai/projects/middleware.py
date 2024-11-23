# projects/middleware.py

from django.conf import settings
from .models.analytics import PageVisit
import re

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exclude_paths = getattr(settings, 'PAGE_ANALYTICS', {}).get('EXCLUDE_PATHS', [])
        self.exclude_patterns = [re.compile(pattern) for pattern in self.exclude_paths]

    def __call__(self, request):
        response = self.get_response(request)
        
        # Skip tracking for excluded paths
        if any(pattern.match(request.path) for pattern in self.exclude_patterns):
            return response

        # Skip tracking for excluded user groups
        if request.user.is_authenticated:
            excluded_groups = getattr(settings, 'PAGE_ANALYTICS', {}).get('EXCLUDE_USER_GROUPS', [])
            if any(group.name in excluded_groups for group in request.user.groups.all()):
                return response

        # Create page visit record
        PageVisit.objects.create(
            path=request.path,
            user=request.user if request.user.is_authenticated else None,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            referrer=request.META.get('HTTP_REFERER', ''),
            device_type=self.get_device_type(request),
            browser=self.get_browser(request)
        )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_device_type(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'mobile' in user_agent:
            return 'mobile'
        elif 'tablet' in user_agent:
            return 'tablet'
        return 'desktop'

    def get_browser(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'chrome' in user_agent:
            return 'chrome'
        elif 'firefox' in user_agent:
            return 'firefox'
        elif 'safari' in user_agent:
            return 'safari'
        elif 'edge' in user_agent:
            return 'edge'
        return 'other'