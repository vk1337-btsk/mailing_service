from django.core.cache import cache

from apps.blog.models import Articles
from config import settings


def get_article_list_from_cache():
    if settings.CACHE_ENABLED:
        key = 'articles_list'
        articles_list = cache.get(key)
        if articles_list is None:
            articles_list = Articles.objects.filter(is_published=True)
            cache.set(key, articles_list)
    else:
        articles_list = Articles.objects.filter(is_published=True)

    return articles_list
