# projects/decorators.py

from functools import wraps
from .models.analytics import EventTracker
import json

def track_event(event_type, get_metadata=None):
    """
    Decorator to track events
    
    @track_event('view')
    @track_event('action', get_metadata=lambda request, *args, **kwargs: {'project_id': kwargs.get('pk')})
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Get the response first
            response = view_func(request, *args, **kwargs)
            
            try:
                # Get metadata if function provided
                metadata = {}
                if get_metadata:
                    metadata = get_metadata(request, *args, **kwargs)
                
                # Create event
                EventTracker.objects.create(
                    event_type=event_type,
                    user=request.user if request.user.is_authenticated else None,
                    path=request.path,
                    target=request.POST.get('target', ''),
                    metadata=metadata
                )
            except Exception as e:
                # Log the error but don't affect the response
                print(f"Error tracking event: {str(e)}")
            
            return response
        return wrapped_view
    return decorator