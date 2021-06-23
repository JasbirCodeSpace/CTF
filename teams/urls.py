from django.urls import path
from .views import team_create, team_join, team_view

urlpatterns = [
    path('create', team_create, name='team-create'),
    path('join', team_join, name='team-join'),
    path('view', team_view, name='team-view')
]