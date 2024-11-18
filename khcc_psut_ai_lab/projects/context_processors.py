# projects/context_processors.py

from django.conf import settings
from .models import Project, UserProfile

def site_context(request):
    """
    Add common context variables to all templates
    """
    context = {
        'site_name': settings.SITE_NAME,
        'site_url': settings.SITE_URL,
    }
    
    if request.user.is_authenticated:
        # Get unread notifications count
        context['unread_notifications_count'] = request.user.notifications.filter(
            is_read=False
        ).count()
        
        # Get user's bookmarked projects
        context['bookmarked_projects'] = Project.objects.filter(
            bookmarks__user=request.user
        ).values_list('id', flat=True)
        
        # Check if user has completed their profile
        try:
            profile = request.user.profile
            context['profile_completed'] = all([
                profile.bio,
                profile.location,
                profile.avatar
            ])
        except UserProfile.DoesNotExist:
            context['profile_completed'] = False
    
    return context

def notifications_processor(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        recent_notifications = request.user.notifications.all()[:5]
        return {
            'unread_notifications_count': unread_count,
            'notifications': recent_notifications,
        }
    return {}