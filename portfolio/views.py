from django.shortcuts import render, get_object_or_404
from .models import Work, Tag, Event, Image, Collaborator


def works(request, tag_slug=None):
    works = Work.objects.filter(featured=True).order_by('-created_date')
    if tag_slug is not None:
        works = works.filter(tags__slug=tag_slug)

    return render(request, 'portfolio/index.html', {
        'works': works,
        'tags': Tag.objects.all(),
        'tag_slug': tag_slug,
    })


def work(request, work_slug):
    work = get_object_or_404(Work, slug=work_slug)
    return render(request, 'portfolio/work.html', {
        'work': work,
        'images': work.images.all(),
        'audios': work.audio.all(),
    })


def events(request):
    return render(request, 'portfolio/events.html', {
        'events': Event.objects.order_by('-date'),
    })


def info(request):
    return render(request, 'portfolio/info.html', {
        'profile': get_object_or_404(Work, title='Profile'),
        'headshot': get_object_or_404(Image, title='profile'),
        'collaborators': Collaborator.objects.order_by('name'),
    })
