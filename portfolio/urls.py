from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tag_slug>[-\w]+)/$', views.filtered, name='filtered'),
    url(r'^all/(?P<work_slug>[-\w]+)/$', views.works, name='work'),
    url(r'^(?P<tag_slug>[-\w]+)/(?P<work_slug>[-\w]+)/$', views.filtered_works, name='work'),
]
