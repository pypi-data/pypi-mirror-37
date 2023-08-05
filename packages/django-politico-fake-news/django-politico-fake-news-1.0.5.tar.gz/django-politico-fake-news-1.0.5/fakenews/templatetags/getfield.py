from django import template
register = template.Library()


@register.filter
def getfield(dict, key):
    return getattr(dict, key)
