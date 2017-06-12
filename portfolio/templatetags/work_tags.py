from django import template
from portfolio.models import Work

register = template.Library()


@register.simple_tag
def get_filtered_works(tag):
    works = Work.objects.order_by('-created_date')
    return works.filter(tags__title=tag)


@register.simple_tag
def get_remaining_works(tag):
    works = Work.objects.order_by('-created_date')
    return works.exclude(tags__title=tag)
