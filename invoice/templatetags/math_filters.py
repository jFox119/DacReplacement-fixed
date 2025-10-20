from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
    
@register.filter
def currency(value):
    """
    Formats a number as currency (e.g., $1,234.57).
    """
    if value is None:
        return ""
    try:
        # Ensure the value is a Decimal for precision
        value = decimal.Decimal(value) 
        # Round to two decimal places
        rounded_value = round(value, 2)
        # Separate integer and decimal parts
        int_part = int(rounded_value)
        dec_part = ("%0.2f" % rounded_value)[-3:]
        # Use intcomma for thousands separation on the integer part
        return "$%s%s" % (intcomma(int_part), dec_part)
    except (ValueError, TypeError, decimal.InvalidOperation):
        return value