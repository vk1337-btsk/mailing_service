from django.urls import path
from django.views.decorators.cache import cache_page

from apps.blog.apps import BlogConfig
from apps.blog.views import (ArticlesListView, ArticlesDetailView, ArticleCreateView, ArticleDeleteView,
                             ArticleUpdateView)

app_name = BlogConfig.name


urlpatterns = [
    path('news/', ArticlesListView.as_view(), name='articles_list'),
    path('news/create/', ArticleCreateView.as_view(), name='create_article'),
    path('news/<str:slug>/', cache_page(60)(ArticlesDetailView.as_view()), name='article'),
    path('news/edit/<str:slug>/', ArticleUpdateView.as_view(), name='update_article'),
    path('news/delete/<str:slug>/', ArticleDeleteView.as_view(), name='delete_article'),

]
