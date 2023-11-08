from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^info/$', views.info, name='info'),
    re_path(r'^events/$', views.events, name='events'),
    re_path(r'^works/$', views.works, name='works'),
    re_path(r'^(?P<tag_slug>[-\w]+)/$', views.works, name='works'),
    re_path(r'^works/(?P<work_slug>[-\w]+)/$', views.work, name='work'),
    re_path(r'^miscellany/$', views.miscellany, name='miscellany'),
]
