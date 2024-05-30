from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main')),
    path('', include('apps.blog.urls', namespace='blog')),
    path('', include('apps.newsletters.urls', namespace='newsletters')),
    path('', include('apps.users.urls', namespace='users')),
    path('', include('apps.clients.urls', namespace='clients')),
    path('', include('apps.messages_.urls', namespace='messages_')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
