import logging

from django import template
from apps.newsletters.models import Newsletters
register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def compare_status(status):
    for data in Newsletters.StateOfMailing.choices:
        if data[0] == status:
            return data[1]


@register.filter
def compare_periodicity(periodicity):
    for data in Newsletters.PeriodicityOfMailing.choices:
        if data[0] == periodicity:
            return data[1]


@register.filter
def media_url(data) -> str:
    if data:
        return f"/media/{data}"
    return "#"


@register.filter
def check_group_manager(user) -> bool:
    return user.groups.filter(name='manager').exists()


@register.filter
def correct_ending_mailings(amount: int) -> str:
    declensions = ['рассылка', 'рассылки', 'рассылок']
    if amount in [5, 6, 7, 8, 9] or amount % 10 in [0, 5, 6, 7, 8, 9] or 11 <= amount % 100 <= 19:
        return f"{amount} {declensions[2]}"
    elif amount in [2, 3, 4] or amount % 10 in [2, 3, 4]:
        return f"{amount} {declensions[1]}"
    else:
        return f"{amount} {declensions[0]}"


@register.filter
def correct_ending_active(amount: int) -> str:
    declensions = ['активных', 'активные', 'активных']
    if amount in [5, 6, 7, 8, 9] or amount % 10 in [0, 5, 6, 7, 8, 9] or 11 <= amount % 100 <= 19:
        return f"{amount} {declensions[2]}"
    elif amount in [2, 3, 4] or amount % 10 in [2, 3, 4]:
        return f"{amount} {declensions[1]}"
    else:
        return f"{amount} {declensions[0]}"


@register.filter
def correct_ending_clients(amount: int) -> str:
    declensions = ['клиент', 'клиента', 'клиентов']
    if amount in [5, 6, 7, 8, 9] or amount % 10 in [0, 5, 6, 7, 8, 9] or 11 <= amount % 100 <= 19:
        return f"{amount} {declensions[2]}"
    elif amount in [2, 3, 4] or amount % 10 in [2, 3, 4]:
        return f"{amount} {declensions[1]}"
    else:
        return f"{amount} {declensions[0]}"


@register.filter
def first_letter(string: str) -> str:
    return string[0]