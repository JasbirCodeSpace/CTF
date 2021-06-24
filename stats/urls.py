from django.urls import path
from .views import profile, team
urlpatterns = [
    path('profile/solves/<str:username>', profile.solves_pie_chart, name='profile-solves-pie-chart'),
    path('profile/category/<str:username>', profile.category_pie_chart, name = 'profile-category-pie-chart'),
    path('team/solves/<str:teamname>', team.solves_pie_chart, name='team-solves-pie-chart'),
    path('team/category/<str:teamname>', team.category_pie_chart, name = 'team-category-pie-chart'),
]