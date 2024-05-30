from django.urls import path

from apps.main.apps import MainConfig
from apps.main.views import HomeView, AboutView, ContactsView

app_name = MainConfig.name


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
