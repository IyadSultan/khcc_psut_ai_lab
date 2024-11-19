from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Splits a string into a list on the given delimiter
    Usage: {{ value|split:"," }}
    """
    return [x.strip() for x in value.split(arg)]