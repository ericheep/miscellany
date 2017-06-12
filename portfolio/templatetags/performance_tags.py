from django import template
from portfolio.models import Performance

register = template.Library()


@register.simple_tag
def get_performances():
    return Performance.objects.order_by('-date')
