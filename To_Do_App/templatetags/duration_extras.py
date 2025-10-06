from django import template

register = template.Library()

@register.filter
def format_duration(value):
    """Convert a timedelta to HH:MM:SS string"""
    if not value:
        return "00:00:00"
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

@register.filter
def seconds(value):
    """Convert timedelta to total seconds"""
    if not value:
        return 0
    return int(value.total_seconds())

@register.simple_tag(takes_context=True)
def active(context, url_name):
    """Returns 'active' if current page matches the given URL name."""
    try:
        if context['request'].resolver_match.url_name == url_name:
            return 'bg-gray-300 text-black font-semibold'
    except Exception:
        pass
    return ''