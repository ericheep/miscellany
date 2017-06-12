from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tag>[-\w]+)/$', views.filtered, name='filtered'),
    url(r'^(?P<slug>[-\w]+)/$', views.work, name='work'),
]
