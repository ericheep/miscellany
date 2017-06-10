from django.shortcuts import render, get_object_or_404
from .models import Work


def index(request):
    return render(request, 'portfolio/index.html')


def work(request, slug):
    work = get_object_or_404(Work, slug=slug)

    context = {
        'work': work,
        'slug': work.slug,
        'title': work.title,
        'text': work.text,
        'date': work.created_date,
        'tags': work.tags,
    }

    return render(request, 'portfolio/work.html', context)
