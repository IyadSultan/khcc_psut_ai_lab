from django.utils import timezone
from .models import PageVisit, VisitorSession
from django.contrib.contenttypes.models import ContentType
import user_agents

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        start_time = timezone.now()
        
        response = self.get_response(request)
        
        # Skip static and admin URLs
        if not any(path in request.path for path in ['/static/', '/admin/', '/media/']):
            # Get or create session
            session_key = request.session.session_key or 'anonymous'
            
            # Parse user agent
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = user_agents.parse(user_agent_string)
            
            # Get visitor session
            visitor_session, created = VisitorSession.objects.get_or_create(
                session_key=session_key,
                defaults={
                    'user': request.user if request.user.is_authenticated else None,
                    'ip_address': self.get_client_ip(request),
                    'user_agent': user_agent_string,
                    'device_type': self.get_device_type(user_agent),
                    'browser': user_agent.browser.family,
                    'os': user_agent.os.family,
                }
            )
            
            # Create page visit
            visit = PageVisit.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=session_key,
                ip_address=self.get_client_ip(request),
                user_agent=user_agent_string,
                path=request.path,
                referer=request.META.get('HTTP_REFERER'),
                time_spent=timezone.now() - start_time
            )
            
            # Try to get content object
            try:
                if hasattr(request, 'resolver_match'):
                    view_kwargs = request.resolver_match.kwargs
                    if 'pk' in view_kwargs:
                        model_name = request.resolver_match.url_name.split('_')[0]
                        content_type = ContentType.objects.get(model=model_name)
                        visit.content_type = content_type
                        visit.object_id = view_kwargs['pk']
                        visit.save()
            except:
                pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def get_device_type(self, user_agent):
        if user_agent.is_mobile:
            return 'mobile'
        elif user_agent.is_tablet:
            return 'tablet'
        return 'desktop' 