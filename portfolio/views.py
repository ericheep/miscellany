from django.shortcuts import render, get_object_or_404
from .models import Work, Tag


def index(request):
    context = {
        'tag_slug': "all",
    }

    return render(request, 'portfolio/index.html', context)


def works(request, work_slug=None):
    works = Work.objects.all().order_by('-created_date')
    tags = Tag.objects.all()

    context = {
        'works': works,
        'tags': tags,
    }

    if work_slug is not None:
        work = get_object_or_404(Work, slug=work_slug)

        context.update({
            'work': work,
            'slug': work.slug,
            'title': work.title,
            'text': work.text,
            'created_date': work.created_date,
        })

    return render(request, 'portfolio/works.html', context)


def contact(request):

    context = {}

    return render(request, 'portfolio/contact.html', context)


def filtered_works(request, tag_slug, work_slug):
    work = get_object_or_404(Work, slug=work_slug)
    tag = get_object_or_404(Tag, slug=tag_slug)

    context = {
        'work': work,
        'slug': work.slug,
        'title': work.title,
        'text': work.text,
        'created_date': work.created_date,

        'tag': tag,
        'tag_slug': tag_slug,
    }

    return render(request, 'portfolio/work.html', context)
