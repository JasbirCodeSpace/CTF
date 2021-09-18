from django.urls import path
from teams import views

urlpatterns = [
    path('create/', views.team_create, name='team-create'),
    path('join/', views.team_join, name='team-join'),
    path('view/<str:teamname>/', views.team_view, name='team-view'),
    path('update/<int:pk>', views.team_update, name='team-update'),
    path('capatain/<int:pk>', views.team_captain_change, name='team-captain'),
    path('delete/<int:pk>', views.team_delete, name='team-delete'),
    path('invite/<str:teamname>/', views.team_invite, name='team-invite'),
    path('choice/', views.team_choice, name='team-choice'),
    path('leave/<int:pk>', views.team_leave, name='team-leave'),
]