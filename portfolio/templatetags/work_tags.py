from django import template
from portfolio.models import Work

register = template.Library()


@register.simple_tag
def get_filtered_works(tag_slug):
    if tag_slug == "all":
        return Work.objects.all().order_by("-created_date")
    else:
        works = Work.objects.all().order_by("-created_date")
        return works.filter(tags__slug=tag_slug)


@register.simple_tag
def get_excluded_works(tag_slug):
    works = Work.objects.all().order_by("-created_date")
    return works.exclude(tags__slug=tag_slug)
