from django import template
from satchmo_utils.templatetags import get_filter_args

register = template.Library()

def prepaid_order_summary(order):
    """Output a formatted block giving attached gift certifificate details."""
    return {'order' : order}
    
register.inclusion_tag('prepaid/_order_summary.html')(prepaid_order_summary)
