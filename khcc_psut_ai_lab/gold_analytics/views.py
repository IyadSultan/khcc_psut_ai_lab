from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg, F, ExpressionWrapper, fields
from django.db.models.functions import TruncDate, TruncHour
from django.utils import timezone
from datetime import timedelta
from .models import PageVisit, VisitorSession, PageMetrics
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return super().default(obj)

@method_decorator(staff_member_required, name='dispatch')
class AnalyticsDashboardView(TemplateView):
    template_name = 'gold_analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Time ranges
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)
        
        # Get basic metrics
        context.update({
            'total_visits': PageVisit.objects.count(),
            'unique_visitors': VisitorSession.objects.count(),
            'avg_session_duration': self.get_avg_session_duration(),
            'bounce_rate': self.get_bounce_rate(),
            
            # Time-based metrics
            'visits_24h': self.get_visits_count(last_24h),
            'visits_7d': self.get_visits_count(last_7d),
            'visits_30d': self.get_visits_count(last_30d),
            
            # Popular pages
            'popular_pages': self.get_popular_pages(),
            
            # Device metrics
            'device_breakdown': self.get_device_breakdown(),
            
            # Traffic sources
            'traffic_sources': self.get_traffic_sources(),
            
            # Visitor flow
            'visitor_flow': self.get_visitor_flow(),
            
            # Charts data with datetime serialization
            'hourly_visits': json.dumps(
                list(self.get_hourly_visits()), 
                cls=DateTimeEncoder
            ),
            'daily_visits': json.dumps(
                list(self.get_daily_visits()), 
                cls=DateTimeEncoder
            ),
        })
        
        return context

    def get_visits_count(self, since):
        return PageVisit.objects.filter(timestamp__gte=since).count()

    def get_avg_session_duration(self):
        return VisitorSession.objects.filter(
            end_time__isnull=False
        ).aggregate(
            avg_duration=Avg(F('end_time') - F('start_time'))
        )['avg_duration']

    def get_bounce_rate(self):
        total_sessions = VisitorSession.objects.count()
        bounce_sessions = PageVisit.objects.values('session_key').annotate(
            visit_count=Count('id')
        ).filter(visit_count=1).count()
        
        return (bounce_sessions / total_sessions * 100) if total_sessions > 0 else 0

    def get_popular_pages(self):
        return PageVisit.objects.values('path').annotate(
            visit_count=Count('id'),
            avg_time=Avg('time_spent')
        ).order_by('-visit_count')[:10]

    def get_device_breakdown(self):
        return VisitorSession.objects.values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')

    def get_traffic_sources(self):
        return PageVisit.objects.values('referer').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

    def get_visitor_flow(self):
        # Modified to work without ArrayAgg
        visitor_paths = []
        sessions = PageVisit.objects.values('session_key').annotate(
            path_count=Count('path')
        ).filter(path_count__gt=1)[:100]
        
        for session in sessions:
            paths = PageVisit.objects.filter(
                session_key=session['session_key']
            ).order_by('timestamp').values_list('path', flat=True)
            visitor_paths.append({
                'session_key': session['session_key'],
                'paths': list(paths)
            })
        
        return visitor_paths

    def get_hourly_visits(self):
        last_24h = timezone.now() - timedelta(hours=24)
        return PageVisit.objects.filter(
            timestamp__gte=last_24h
        ).annotate(
            hour=TruncHour('timestamp')
        ).values('hour').annotate(
            count=Count('id')
        ).order_by('hour').values('hour', 'count')

    def get_daily_visits(self):
        last_30d = timezone.now() - timedelta(days=30)
        return PageVisit.objects.filter(
            timestamp__gte=last_30d
        ).annotate(
            date=TruncDate('timestamp')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date').values('date', 'count')