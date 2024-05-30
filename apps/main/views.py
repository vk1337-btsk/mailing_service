import logging
import random

from django.views.generic import TemplateView

from apps.blog.models import Articles
from core.services import get_random_articles, get_count_newsletters, get_count_active_newsletters, get_count_clients

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'main/home.html'
    extra_context = {'title': 'Главная'}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['random_articles_list'] = get_random_articles(4)
        context_data['count_newsletters'] = get_count_newsletters()
        context_data['count_active_newsletters'] = get_count_active_newsletters()
        context_data['count_clients'] = get_count_clients()
        return context_data


class AboutView(TemplateView):
    template_name = 'main/about.html'
    extra_context = {'title': 'О нас'}


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'
    extra_context = {'title': 'Контакты'}
