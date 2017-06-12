from django.shortcuts import render, get_object_or_404
from .models import Work


def index(request):
    return render(request, 'portfolio/index.html')


def filtered(request, tag):
    works = Work.objects.all()

    filtered_works = works.filter(tags__title=tag)
    excluded_works = works.exclude(tags__title=tag)

    context = {
        'filtered_works': filtered_works,
        'excluded_works': excluded_works,
        'tag': tag,
    }

    return render(request, 'portfolio/filtered.html', context)


def work(request, slug):
    work = get_object_or_404(Work, slug=slug)

    context = {
        'work': work,
        'slug': work.slug,
        'title': work.title,
        'text': work.text,
        'date': work.created_date,
    }

    return render(request, 'portfolio/work.html', context)
