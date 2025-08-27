from django import template

register = template.Library()

@register.filter
def dictkey(d, key):
    """
    Usage: {{ mydict|dictkey:some_key }}
    Returns d[key] if present, else None.
    """
    if isinstance(d, dict):
        return d.get(key)
    return None
