from django import template
from portfolio.models import Work

register = template.Library()


@register.simple_tag
def get_works():
    return Work.objects.order_by('-created_date')
