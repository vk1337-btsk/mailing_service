from django.urls import path

from apps.newsletters.apps import NewsletterConfig
from apps.newsletters.views import (NewslettersListView, NewsletterDetailView, NewsletterCreateView,
                                    NewsletterUpdateView, NewsletterDeleteView, set_newsletters_status)

app_name = NewsletterConfig.name


urlpatterns = [
    path('newsletters/', NewslettersListView.as_view(), name='newsletters_list'),
    path('newsletters/<int:pk>', NewsletterDetailView.as_view(), name='newsletter'),
    path('newsletters/create/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('newsletters/update/<int:pk>/', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('newsletters/delete/<int:pk>/', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('setnewslettersstatus/<int:pk>/', set_newsletters_status, name='set_newsletters_status'),
]
