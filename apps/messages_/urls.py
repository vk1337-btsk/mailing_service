from django.urls import path
from apps.messages_.apps import MessagesConfig
from apps.messages_.views import MessagesListView, MessageCreateView, MessageDetailView, MessageDeleteView, \
    MessageUpdateView

app_name = MessagesConfig.name


urlpatterns = [
    path('messages/', MessagesListView.as_view(), name='messages_list'),

    path('messages/<int:pk>', MessageDetailView.as_view(), name='message'),
    path('messages/create/', MessageCreateView.as_view(), name='create_message'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

]
