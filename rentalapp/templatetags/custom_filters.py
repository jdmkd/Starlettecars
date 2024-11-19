from django import template

register = template.Library()

@register.filter
def add(value, arg):
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

    
@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0
    

