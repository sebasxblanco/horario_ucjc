from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """{{ dict|get_item:key }} — acceso a dict con clave dinámica en templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
