from django.urls import path

from apps.newsletters.apps import NewsletterConfig
from apps.clients.views import (ClientsListView, ClientDetailView, ClientCreateView, ClientUpdateView,
                                ClientDeleteView, AddClientsToNewsletterView)

app_name = NewsletterConfig.name

urlpatterns = [
    path('clients/', ClientsListView.as_view(), name='clients_list'),
    path('client/<int:pk>', ClientDetailView.as_view(), name='client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('newsletters/<int:newsletter_id>/add_clients/', AddClientsToNewsletterView.as_view(),
         name='add_clients'),
]
