import django_filters
from django.db.models import Q
from ..models import Project

class ProjectFilter(django_filters.FilterSet):
    """FilterSet for advanced project filtering"""
    query = django_filters.CharFilter(method='filter_query')
    tags = django_filters.CharFilter(method='filter_tags')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    min_claps = django_filters.NumberFilter(field_name='claps', lookup_expr='gte')
    has_github = django_filters.BooleanFilter(method='filter_has_github')
    
    class Meta:
        model = Project
        fields = ['query', 'tags', 'date_from', 'date_to', 'min_claps', 'has_github']
    
    def filter_query(self, queryset, name, value):
        if not value:
            return queryset
        
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(author__username__icontains=value) |
            Q(tags__icontains=value)
        )
    
    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        
        tags = [tag.strip().lower() for tag in value.split(',') if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset
    
    def filter_has_github(self, queryset, name, value):
        if value:
            return queryset.exclude(github_link='')
        return queryset