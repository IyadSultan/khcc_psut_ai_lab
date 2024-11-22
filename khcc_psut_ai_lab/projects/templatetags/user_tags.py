from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def is_faculty(user):
    """Check if user is in the Faculty group"""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='Faculty').exists()