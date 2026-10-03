from django.contrib import admin
from .models import Work, Event, Venue, Image, Tag, Collaborator, Audio


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'abstract', 'created_date', 'featured']
    list_filter = ['featured', 'tags']
    search_fields = ['title', 'abstract', 'text']
    ordering = ['-created_date']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'venue']
    ordering = ['-date']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    search_fields = ['title']


admin.site.register([Venue, Audio, Tag, Collaborator])
