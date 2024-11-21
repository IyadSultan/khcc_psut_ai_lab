# templatetags/query_tags.py

from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag
def query_transform(request_get, param_name, value, action='add'):
    """
    Transform query parameters while preserving other parameters
    """
    updated = request_get.copy()
    
    if action == 'remove':
        # Remove a specific value from a comma-separated list
        current_values = updated.get(param_name, '').split(',')
        current_values = [v for v in current_values if v and v != value]
        if current_values:
            updated[param_name] = ','.join(current_values)
        else:
            updated.pop(param_name, None)
    else:
        # Add or replace value
        if value:
            updated[param_name] = value
        else:
            updated.pop(param_name, None)
    
    return '?' + urlencode(updated)