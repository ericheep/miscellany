from django.contrib import admin
from .models import Work, Performance, Venue, Image


class WorkAdmin(admin.ModelAdmin):
    list_display = ["__str__", "slug", "discipline", "tags", "created_date"]

    class Meta:
        model = Work


admin.site.register(Work, WorkAdmin)
admin.site.register(Performance)
admin.site.register(Venue)
admin.site.register(Image)
