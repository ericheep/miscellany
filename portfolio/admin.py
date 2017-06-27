from django.contrib import admin
from .models import Work, Performance, Venue, Image, Tag, Collaborator


class WorkAdmin(admin.ModelAdmin):
    list_display = ["__str__", "slug", "short_text", "created_date"]

    class Meta:
        model = Work


class PerformanceAdmin(admin.ModelAdmin):

    class Meta:
        model = Performance


admin.site.register(Work, WorkAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Venue)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Collaborator)
