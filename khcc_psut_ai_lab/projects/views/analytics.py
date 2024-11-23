# projects/views/analytics.py

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.shortcuts import render
from ..models.analytics import PageVisit, EventTracker

@staff_member_required
def analytics_dashboard(request):
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timezone.timedelta(days=days)

    # Get basic stats
    total_visits = PageVisit.objects.filter(timestamp__gte=start_date).count()
    unique_visitors = PageVisit.objects.filter(timestamp__gte=start_date).values('user', 'ip_address').distinct().count()
    
    # Get daily visits
    daily_visits = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        date=TruncDate('timestamp')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Get popular pages
    popular_pages = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).values('path').annotate(
        visits=Count('id')
    ).order_by('-visits')[:10]

    # Get device breakdown
    devices = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).values('device_type').annotate(
        count=Count('id')
    )

    # Get browser breakdown
    browsers = PageVisit.objects.filter(
        timestamp__gte=start_date
    ).values('browser').annotate(
        count=Count('id')
    )

    context = {
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'daily_visits': daily_visits,
        'popular_pages': popular_pages,
        'devices': devices,
        'browsers': browsers,
        'days': days,
    }

    return render(request, 'analytics/dashboard.html', context)