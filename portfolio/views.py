import random

from django.shortcuts import render, get_object_or_404
from .forms import WorkForm, EventForm, VenueForm, ImageForm
from .models import Work, Tag, Event, Venue, Image, Collaborator


def index(request):

    random_p5 = random.choice(['slow-shapes.js', 'paths.js'])

    context = {
        'random_p5': random_p5,
    }

    return render(request, 'portfolio/index.html', context)


def works(request, tag_slug=None):
    works = Work.objects.all().filter(featured=True).order_by('-created_date')
    tags = Tag.objects.all()

    if tag_slug is not None:
        works = works.filter(tags__slug=tag_slug)

    context = {
        'works': works,
        'tags': tags,
        'tag_slug': tag_slug,
    }

    return render(request, 'portfolio/works.html', context)


def work(request, work_slug):
    work = get_object_or_404(Work, slug=work_slug)
    images = work.images.all()
    audios = work.audio.all()

    context = {
        'work': work,
        'images': images,
        'audios': audios,
    }

    return render(request, 'portfolio/work.html', context)


def events(request):
    events = Event.objects.all().order_by('-date')

    context = {
        'events': events,
    }

    return render(request, 'portfolio/events.html', context)


def about(request):
    profile = get_object_or_404(Work, title="Profile")
    headshot = get_object_or_404(Image, title='profile')
    collaborators = Collaborator.objects.all().order_by('name')

    context = {
        'profile': profile,
        'headshot': headshot,
        'collaborators': collaborators,
    }

    return render(request, 'portfolio/about.html', context)


def miscellany(request):

    work_form = WorkForm()
    event_form = EventForm()
    venue_form = VenueForm()
    image_form = ImageForm()

    works = Work.objects.all().order_by('-created_date')
    events = Event.objects.all().order_by('-date')
    venues = Venue.objects.all().order_by('name')
    images = Image.objects.all().order_by('title')

    context = {
        'work_form': work_form,
        'event_form': event_form,
        'venue_form': venue_form,
        'image_form': image_form,
        'works': works,
        'events': events,
        'venues': venues,
        'images': images,
    }

    return render(request, 'portfolio/miscellany.html', context)
