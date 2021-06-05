from django.urls import path
from .views import challenges
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', challenges, name='challenges'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 