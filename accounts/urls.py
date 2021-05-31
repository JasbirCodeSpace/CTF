from django.urls import path
from .views.profile import profile_login, profile_register, profile_logout
urlpatterns = [
    path('register/', profile_register, name='profile-register'),
    path('login/', profile_login, name = 'profile-login'),
    path('logout/', profile_logout, name='profile-logout'),
]