from django.urls import path
from .views import profile, team
urlpatterns = [
    path('profile/solves/', profile.solves_pie_chart, name='profile-solves-pie-chart'),
    path('profile/category/', profile.category_pie_chart, name = 'profile-category-pie-chart'),
    path('team/solves/', team.solves_pie_chart, name='team-solves-pie-chart'),
    path('team/category/', team.category_pie_chart, name = 'team-category-pie-chart'),
]