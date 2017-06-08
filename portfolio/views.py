from django.shortcuts import render, get_object_or_404
from .models import Work


def portfolio(request, slug):
    # works = Work.objects.order_by('created_date')
    # works = Work.objects.values_list('text', flat=True).order_by('created_date')
    # performances = Performance.objects.order_by('date')

    work = get_object_or_404(Work, slug=slug)

    context = {
        'work': work,
        'slug': slug,
        'title': work.title,
        'text': work.text,
        'date': work.created_date,
    }

    return render(request, 'portfolio/portfolio.html', context)
