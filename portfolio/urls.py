from django.urls import path
from . import views

urlpatterns = [
    path('', views.works, name='index'),
    path('info/', views.info, name='info'),
    path('events/', views.events, name='events'),
    path('works/', views.works, name='works'),
    path('works/<slug:work_slug>/', views.work, name='work'),
    path('<slug:tag_slug>/', views.works, name='works'),
]
