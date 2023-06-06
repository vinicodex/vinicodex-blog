from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [

    path('', views.index, name='index'),
    path('projects', views.projects, name='projects'),
    path('contact', views.projects, name='contact'),
]