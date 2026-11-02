from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from .models import Work, Tag, Event, Collaborator


def works(request, tag_slug=None):
    # Ongoing works first; then by most recent date (end date if any, else start)
    works = (Work.objects.filter(featured=True)
             .annotate(recent=Coalesce('end_date', 'created_date'))
             .order_by('-ongoing', '-recent', '-created_date'))
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
    """The info page is the work titled 'Profile', shown like any other work."""
    profile = get_object_or_404(Work, title='Profile')
    return render(request, 'portfolio/work.html', {
        'work': profile,
        'images': profile.images.all(),
        'audios': profile.audio.all(),
        'is_info': True,  # no title/date card; collaborators listed at the end
        'collaborators': Collaborator.objects.order_by('name'),
    })
