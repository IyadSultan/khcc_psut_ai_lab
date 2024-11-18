# projects/templatetags/project_tags.py

from django import template
from django.db.models import Q
from ..models import Project

register = template.Library()

@register.simple_tag
def get_similar_projects(project):
    """Returns similar projects based on tags"""
    if not project.tags:
        return Project.objects.exclude(id=project.id)[:3]
    
    tags = [tag.strip() for tag in project.tags.split(',')]
    similar_projects = Project.objects.filter(
        tags__icontains=tags[0]
    ).exclude(id=project.id)
    
    for tag in tags[1:]:
        similar_projects = similar_projects | Project.objects.filter(
            tags__icontains=tag
        ).exclude(id=project.id)
    
    return similar_projects.distinct()[:3]