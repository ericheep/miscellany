from django.contrib import admin
from .models import Work, Event, Venue, Image, Tag, Collaborator, Audio


class WorkAdmin(admin.ModelAdmin):
    list_display = ["__str__", "abstract", "created_date"]
    ordering = ('-created_date',)

    class Meta:
        model = Work


class EventAdmin(admin.ModelAdmin):

    class Meta:
        model = Event


admin.site.register(Work, WorkAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Venue)
admin.site.register(Audio)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Collaborator)
