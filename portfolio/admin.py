from datetime import date

from django import forms
from django.contrib import admin
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import path, reverse
from django.utils.dateparse import parse_date
from django.utils.text import slugify

from .models import Work, Event, Venue, Image, Tag, Collaborator, Audio
from .uploads import UploadError, save_upload


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'abstract', 'created_date', 'featured']
    list_filter = ['featured', 'tags']
    search_fields = ['title', 'abstract', 'text', 'body']
    ordering = ['-created_date']

    class Media:
        js = ['portfolio/admin_body.js']
        css = {'all': ['portfolio/admin_body.css']}

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'body':
            kwargs['widget'] = forms.Textarea(attrs={
                'rows': 30,
                'class': 'vLargeTextField body-editor',
                'data-upload-url': reverse('admin:portfolio_work_upload'),
                'data-preview-url': reverse('admin:portfolio_work_preview'),
            })
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_urls(self):
        # Custom URLs go first: the default ones end in a catch-all for object IDs.
        custom = [
            path('upload/', self.admin_site.admin_view(self.upload_view),
                 name='portfolio_work_upload'),
            path('preview/', self.admin_site.admin_view(self.preview_view),
                 name='portfolio_work_preview'),
        ]
        return custom + super().get_urls()

    def upload_view(self, request):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        uploaded = request.FILES.get('file')
        if not uploaded:
            return JsonResponse({'error': 'no file received'}, status=400)
        try:
            return JsonResponse({'shortcode': save_upload(uploaded)})
        except UploadError as e:
            return JsonResponse({'error': str(e)}, status=400)

    def preview_view(self, request):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        title = request.POST.get('title') or 'Untitled'
        work = Work(
            title=title,
            slug=slugify(title),
            body=request.POST.get('body', ''),
            created_date=parse_date(request.POST.get('created_date', '')) or date.today(),
        )
        return render(request, 'portfolio/work.html', {'work': work, 'images': [], 'audios': []})


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'venue']
    ordering = ['-date']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    search_fields = ['title']


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'audio']
    search_fields = ['title']


admin.site.register([Venue, Tag, Collaborator])
