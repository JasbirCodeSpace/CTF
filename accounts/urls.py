from django.urls import path
from .views.profile import profile_signup
urlpatterns = [
    path('signup/', profile_signup, name='profile-signup'),
]