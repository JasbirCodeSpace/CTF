from django.conf.urls import url
from django.urls import path
from .views import challenges, flagsubmit
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('', challenges, name='challenges'),
    path('flagsubmit', flagsubmit, name='flagsubmit'),
    url(r'^uploads/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 