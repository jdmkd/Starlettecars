from re import template
# from django import template


register = template.Library()

@register.filter
def length_is(value, arg):
    return len(value) == arg
