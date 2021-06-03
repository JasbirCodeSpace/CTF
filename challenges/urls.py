from django.urls import path
from .views import challenges

urlpatterns = [
    path('', challenges, name='challenges'),
]