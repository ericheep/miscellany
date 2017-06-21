from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .forms import WorkForm, PerformanceForm
from .models import Work, Tag, Performance


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


class FilterWorks(View):
    def get(self, request, *args, **kwargs):
        tag = request.GET.get('tag', None)

        works = Work.objects.all()

        if tag:
            works = works.filter()


def about(request):

    context = {}

    return render(request, 'portfolio/about.html', context)


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


def miscellany(request):

    work_form = WorkForm()
    performance_form = PerformanceForm()

    works = Work.objects.all().order_by('-created_date')
    performances = Performance.objects.all().order_by('-date')

    context = {
        'work_form': work_form,
        'performance_form': performance_form,
        'works': works,
        'performances': performances,
    }

    return render(request, 'portfolio/miscellany.html', context)
