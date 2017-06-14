from django import template
from portfolio.models import Tag

register = template.Library()


@register.simple_tag
def get_tags(tag_slug):
    return Tag.objects.exclude(slug=tag_slug)
