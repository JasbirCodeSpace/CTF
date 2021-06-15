from django.urls import path
from .views import challenges, flagsubmit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', challenges, name='challenges'),
    path('flagsubmit', flagsubmit, name='flagsubmit'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 