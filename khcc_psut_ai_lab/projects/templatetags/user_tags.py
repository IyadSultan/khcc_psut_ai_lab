from django import template
from django.contrib.auth.models import User
from projects.models import Follow

register = template.Library()

@register.filter
def is_faculty(user):
    """Check if user is in the Faculty group"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='Faculty').exists()

@register.filter
def is_following(user, target_user):
    """Check if user is following target_user"""
    if not user.is_authenticated:
        return False
    return Follow.objects.filter(follower=user, following=target_user).exists()