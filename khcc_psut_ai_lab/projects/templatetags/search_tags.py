# projects/templatetags/search_tags.py

from django import template
from django.utils.html import mark_safe
from django.utils.html import escape
import re

register = template.Library()

@register.filter(name='highlight')
def highlight_search_term(text, search_term):
    """Highlight search terms in text while preserving HTML safety"""
    if not search_term or not text:
        return text
    
    text = str(text)
    search_term = str(search_term)
    
    # Escape HTML in the text
    text = escape(text)
    
    # Create a pattern that matches whole words
    pattern = r'({})'.format(re.escape(search_term))
    
    # Replace matches with highlighted version
    highlighted = re.sub(
        pattern,
        r'<mark class="highlight">\1</mark>',
        text,
        flags=re.IGNORECASE
    )
    
    return mark_safe(highlighted)

@register.filter(name='querystring_without')
def querystring_without(query_dict, key):
    """Remove a key from querystring while preserving other parameters"""
    query_dict = query_dict.copy()
    query_dict.pop(key, None)
    return query_dict.urlencode()

@register.simple_tag
def url_with_querystring(request, **kwargs):
    """Build URL with updated querystring parameters"""
    query_dict = request.GET.copy()
    for key, value in kwargs.items():
        query_dict[key] = value
    return '?{}'.format(query_dict.urlencode())