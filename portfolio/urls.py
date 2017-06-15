from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^works/$', views.works, name='works'),
    url(r'^works/(?P<work_slug>[-\w]+)/$', views.works, name='works'),
    # url(r'^(?P<tag_slug>[-\w]+)/(?P<work_slug>[-\w]+)/$', views.filtered_works, name='work'),
]

