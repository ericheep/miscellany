from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^events/$', views.events, name='events'),
    url(r'^works/$', views.works, name='works'),
    url(r'^(?P<tag_slug>[-\w]+)/$', views.works, name='works'),
    url(r'^works/(?P<work_slug>[-\w]+)/$', views.work, name='work'),
    url(r'^miscellany/$', views.miscellany, name='miscellany'),
]
