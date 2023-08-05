from django import template
register = template.Library()


@register.filter
def getkey(dict, key):
    return dict[key]
