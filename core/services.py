import random
import secrets
import string

from django.db.models import Count

from apps.blog.models import Articles
from apps.clients.models import Clients
from apps.newsletters.models import Newsletters


def get_random_articles(count: int) -> list:
    queryset_count = Articles.objects.aggregate(count=Count('id'))['count']

    if queryset_count == 0:
        return []

    if count >= queryset_count:
        return list(Articles.objects.all())

    random_indexes = random.sample(range(queryset_count), count)
    random_articles = list(Articles.objects.all()[index] for index in random_indexes)

    return random_articles


def get_count_newsletters() -> int:
    count_newsletters = Newsletters.objects.count()
    return count_newsletters


def get_count_active_newsletters() -> int:
    count_newsletters = Newsletters.objects.filter(is_active=True).count()
    return count_newsletters


def get_count_clients() -> int:
    count_clients = Clients.objects.count()
    return count_clients


def make_random_password():
    character = string.ascii_letters + string.digits
    password = "".join(secrets.choice(character) for _ in range(15))
    return password
