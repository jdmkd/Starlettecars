from django import template
register = template.Library()

@register.filter
def float_to_int(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0

@register.filter
def currency_format(value):
    try:
        value = float(value)
        return f"₹{value:,.0f}"
    except (ValueError, TypeError):
        return "₹value" 