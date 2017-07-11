from django import template
from portfolio.models import Event

register = template.Library()


@register.simple_tag
def get_event():
    return Event.objects.order_by('-date')
