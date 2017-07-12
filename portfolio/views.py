from django.shortcuts import render, get_object_or_404
# from django.views.generic import View

from .forms import WorkForm, EventForm, VenueForm, ImageForm
from .models import Work, Tag, Event, Venue, Image, Collaborator


def index(request):
    context = {
        'tag_slug': "all",
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

    context = {
        'work': work,
    }

    return render(request, 'portfolio/work.html', context)


def about(request):

    images = Image.objects.all().filter(image_type='P')
    image = images.order_by('?').first()
    collaborators = Collaborator.objects.all().order_by('name')

    context = {
        'image': image,
        'collaborators': collaborators,
    }

    return render(request, 'portfolio/about.html', context)


def contact(request):

    context = {}

    return render(request, 'portfolio/contact.html', context)


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
