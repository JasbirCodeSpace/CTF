from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('instructions', views.instructions, name='instructions'),
    path('hackerboard', views.hackerboard, name='hackerboard'),
]